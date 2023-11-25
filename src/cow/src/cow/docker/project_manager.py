from os import environ, makedirs
from os.path import join, exists

from cow.config import ConfigProvider, ProjectConfig
from cow.docker.introspection import DockerInstrospection
from cow.host import Host
from cow.paths import PathsProvider


class ProjectPaths:
    def __init__(
        self, projects_path: str, project_name: str, project_config: ProjectConfig
    ) -> None:
        self._projects_path = projects_path
        self._project_name = project_name
        self._project_config = project_config

    @property
    def base(self):
        return join(self._projects_path, self._project_name)

    @property
    def git_repository(self):
        return join(self.base, "git-repository")

    @property
    def compose_project(self):
        return join(
            self.git_repository, self._project_config.compose.project_path.lstrip("/")
        )


class DockerProjectManager:
    def __init__(
        self,
        host: Host,
        config_provider: ConfigProvider,
        docker_introspection: DockerInstrospection,
        paths_provider: PathsProvider,
    ) -> None:
        self._host = host
        self._config_provider = config_provider
        self._docker_introspection = docker_introspection
        self._paths_provider = paths_provider

    def refresh(self, project_name: str):
        project_config = self.must_get_project_config(project_name)
        project_paths = ProjectPaths(
            self._paths_provider.projects, project_name, project_config
        )
        project_mounted_paths = ProjectPaths(
            self.get_projects_mounted_path(), project_name, project_config
        )

        yield "## Ensuring project's folder exists\n"
        makedirs(project_paths.base, exist_ok=True)

        if exists(project_paths.git_repository):
            yield "## Pulling existing repository\n"
            yield self._host.run(["git", "pull"], cwd=project_paths.git_repository)
        else:
            yield "## Cloning new repository\n"
            yield self._host.run(
                [
                    "git",
                    "clone",
                    project_config.git.repository,
                    project_paths.git_repository,
                ]
            )

        compose_files_args = (
            sum(
                list(
                    ["--file", join(project_paths.compose_project, f)]
                    for f in project_config.compose.compose_files
                ),
                [],
            )
            if project_config.compose.compose_files is not None
            else []
        )

        compose_environment_variables = (
            project_config.compose.environment
            if project_config.compose.environment is not None
            else {}
        )

        yield "## Runnning docker compose\n"
        yield self._host.run(
            [
                "docker",
                "compose",
                "--project-name",
                project_name,
                "--project-directory",
                project_paths.compose_project,
                *compose_files_args,
                "up",
                "--detach",
                "--build",
            ],
            cwd=project_paths.compose_project,
            env=dict(
                environ,
                **compose_environment_variables,
                COW_PROJECT_PATH=project_mounted_paths.compose_project,
            ),
        )
        yield "## Done"

    def must_get_project_config(self, project_name: str) -> ProjectConfig:
        config = self._config_provider.get_config()
        if project_name not in config.projects.keys():
            raise Exception(f"Project {project_name} does not exist")

        return config.projects[project_name]

    def get_projects_mounted_path(self):
        for mount in self._docker_introspection.get_mounts():
            if mount.destination == "/cow":
                return join(mount.source, "projects")

        raise Exception("Could not find the mounted projects path")

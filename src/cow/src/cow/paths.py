from os.path import join


class PathsProvider:
    def get_config_path(self) -> str:
        return "/config/config.toml"

    def get_project_path(self, project_name: str) -> str:
        return join("/projects", project_name)

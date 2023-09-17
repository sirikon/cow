from os import makedirs
from os.path import join, exists
from subprocess import DEVNULL, PIPE, STDOUT, run
from typing import Optional

from cow.di import paths_provider, config_provider
from flask import Flask, abort

app = Flask(__name__)


@app.get("/webhook/<project_name>")
async def webhook_handler(project_name: str):
    config = config_provider.get_config()

    if project_name not in config.projects.keys():
        abort(404)

    project_config = config.projects[project_name]
    project_base_path = paths_provider.get_project_base_path(project_name)
    git_repository_path = join(project_base_path, "git-repository")
    compose_project_path = join(
        git_repository_path, project_config.compose.project_path.lstrip("/")
    )

    def stream_result():
        yield "## Ensuring project's folder exists\n"
        makedirs(project_base_path, exist_ok=True)

        if exists(git_repository_path):
            yield "## Pulling existing repository\n"
            yield cmd(["git", "pull"], cwd=git_repository_path)
        else:
            yield "## Cloning new repository\n"
            yield cmd(
                ["git", "clone", project_config.git.repository, git_repository_path]
            )

        yield "## Runnning docker compose\n"
        yield cmd(
            [
                "docker",
                "compose",
                "--project-name",
                project_name,
                "up",
                "--detach",
                "--build",
            ],
            cwd=compose_project_path,
        )
        yield "## Done"

    return stream_result(), {"Content-Type": "text/plain;charset=utf8"}


def cmd(args: list[str], cwd: Optional[str] = None):
    result = run(args, cwd=cwd, stderr=STDOUT, stdout=PIPE, stdin=DEVNULL, text=True)
    return result.stdout

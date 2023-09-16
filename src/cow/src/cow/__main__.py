from os import makedirs
from os.path import join, exists
from pathlib import Path
from subprocess import run

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
    git_repository_path = join(project_base_path, "git_repository")
    compose_project_path = join(
        git_repository_path, project_config.compose.project_path.lstrip("/")
    )

    makedirs(project_base_path, exist_ok=True)
    if exists(git_repository_path):
        run(["git", "pull"], cwd=git_repository_path)
    else:
        run(["git", "clone", project_config.git.repository, git_repository_path])

    run(["docker", "compose", "up", "-d", "--build"], cwd=compose_project_path)

    return {"ok": True}

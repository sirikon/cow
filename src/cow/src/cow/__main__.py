from cow.di import paths_provider, config_provider
from flask import Flask, abort

app = Flask(__name__)


@app.get("/webhook/<project_name>")
async def hello_world(project_name: str):
    config = config_provider.get_config()

    if project_name not in config.projects.keys():
        abort(404)

    project_config = config.projects[project_name]
    return {
        "config": project_config.model_dump(),
        "path": paths_provider.get_project_path(project_name),
    }

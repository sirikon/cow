import hashlib
import hmac
from os import makedirs, environ
from os.path import join, exists
from subprocess import DEVNULL, PIPE, STDOUT, run
from typing import Optional

from cow.di import (
    config_provider,
    docker_project_manager,
)
from flask import Flask, Request, abort, request

app = Flask(__name__)


@app.post("/webhook/<project_name>")
async def webhook_handler(project_name: str):
    config = config_provider.get_config()
    if project_name not in config.projects.keys():
        abort(404)
    validate_github_signature(request, config.projects[project_name].webhook.secret)

    return docker_project_manager.refresh(project_name), {
        "Content-Type": "text/plain;charset=utf8"
    }


def cmd(args: list[str], cwd: Optional[str] = None, **kwargs):
    result = run(
        args, cwd=cwd, stderr=STDOUT, stdout=PIPE, stdin=DEVNULL, text=True, **kwargs
    )
    return result.stdout


def validate_github_signature(request: Request, secret: str):
    signature = request.headers.get("x-hub-signature-256")
    if signature is None:
        abort(400)

    hash_object = hmac.new(
        secret.encode("utf-8"), msg=request.get_data(), digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        abort(400)

import tomllib
from typing import Optional

from pydantic import BaseModel
from cow.paths import PathsProvider


class ProjectComposeConfig(BaseModel):
    project_path: str
    compose_files: Optional[list[str]]
    environment: Optional[dict[str, str]]


class ProjectGitConfig(BaseModel):
    repository: str


class ProjectWebhookConfig(BaseModel):
    secret: str


class ProjectConfig(BaseModel):
    compose: ProjectComposeConfig
    git: ProjectGitConfig
    webhook: ProjectWebhookConfig


class Config(BaseModel):
    projects: dict[str, ProjectConfig]


class ConfigProvider:
    def __init__(self, paths_provider: PathsProvider) -> None:
        self._paths_provider = paths_provider

    def get_config(self) -> Config:
        with open(self._paths_provider.config, "rb") as f:
            raw_config = tomllib.load(f)
        return Config(**raw_config)

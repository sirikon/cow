import tomllib
from typing import Optional

from pydantic import BaseModel
from cow.paths import PathsProvider


class ConfigProvider:
    def __init__(self, paths_provider: PathsProvider) -> None:
        self._paths_provider = paths_provider

    def get_config(self):
        config_path = self._paths_provider.get_config_path()
        with open(config_path, "rb") as f:
            raw_config = tomllib.load(f)
        return Config(**raw_config)


class Project(BaseModel):
    git_repository: str
    path: Optional[str] = "/"


class Config(BaseModel):
    projects: dict[str, Project]

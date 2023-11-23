from os.path import join


class PathsProvider:
    @property
    def base(self) -> str:
        return "/cow"

    @property
    def config(self) -> str:
        return join(self.base, "config/config.toml")

    @property
    def projects(self) -> str:
        return join(self.base, "projects")

    @property
    def logs(self) -> str:
        return join(self.base, "logs")

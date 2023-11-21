from os.path import join


class PathsProvider:
    def get_config_path(self) -> str:
        return "/config/config.toml"

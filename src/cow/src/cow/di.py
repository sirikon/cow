from cow.config import ConfigProvider
from cow.paths import PathsProvider


paths_provider = PathsProvider()
config_provider = ConfigProvider(paths_provider)

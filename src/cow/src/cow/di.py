from cow.config import ConfigProvider
from cow.docker.introspection import DockerInstrospection
from cow.host import Host
from cow.paths import PathsProvider


host = Host()
docker_introspection = DockerInstrospection(host)
paths_provider = PathsProvider()
config_provider = ConfigProvider(paths_provider)

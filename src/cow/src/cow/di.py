from cow.config import ConfigProvider
from cow.docker.introspection import DockerInstrospection
from cow.docker.project_manager import DockerProjectManager
from cow.host import Host
from cow.paths import PathsProvider


paths_provider = PathsProvider()
config_provider = ConfigProvider(paths_provider)
host = Host()
docker_introspection = DockerInstrospection(host)
docker_project_manager = DockerProjectManager(
    host, config_provider, docker_introspection, paths_provider
)

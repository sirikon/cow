import json
from cow.host import Host


class DockerInstrospection:
    def __init__(self, host: Host) -> None:
        self._host = host

    def get_mounts(self):
        data = json.loads(self._host.run(["bash", "-c", 'docker inspect "$HOSTNAME"']))
        return data[0]["Mounts"]

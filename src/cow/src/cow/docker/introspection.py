from dataclasses import dataclass
import json
from cow.host import Host


@dataclass
class DockerMount:
    source: str
    destination: str


class DockerInstrospection:
    def __init__(self, host: Host) -> None:
        self._host = host

    def get_mounts(self):
        data = json.loads(self._host.run(["bash", "-c", 'docker inspect "$HOSTNAME"']))
        if len(data) == 0:
            return []

        return list(
            DockerMount(m["Source"], m["Destination"]) for m in data[0]["Mounts"]
        )

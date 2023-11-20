import json
from unittest.mock import Mock

from cow.docker.introspection import DockerInstrospection, DockerMount
from cow.host import Host


class TestDockerIntrospection:
    _host = Mock(spec=Host)
    _docker_introspection = DockerInstrospection(_host)

    def test_get_mounts_with_no_matching_containers(self):
        self.given_docker_inspect_result([])
        result = self._docker_introspection.get_mounts()
        assert result == []
        self.assert_docker_inspect_called()

    def test_get_mounts_with_no_mounts(self):
        self.given_docker_inspect_result([{"Mounts": []}])
        result = self._docker_introspection.get_mounts()
        assert result == []
        self.assert_docker_inspect_called()

    def test_get_mounts_with_many_mounts(self):
        self.given_docker_inspect_result(
            [
                {
                    "Mounts": [
                        {
                            "Destination": "/projects",
                            "Source": "/home/johndoe/projects",
                        },
                        {"Destination": "/config", "Source": "/srv/cow/config"},
                    ]
                }
            ]
        )
        result = self._docker_introspection.get_mounts()
        assert result == [
            DockerMount("/home/johndoe/projects", "/projects"),
            DockerMount("/srv/cow/config", "/config"),
        ]
        self.assert_docker_inspect_called()

    def given_docker_inspect_result(self, obj):
        self._host.run.return_value = json.dumps(obj)

    def assert_docker_inspect_called(self):
        self._host.run.assert_called_with(["bash", "-c", 'docker inspect "$HOSTNAME"'])

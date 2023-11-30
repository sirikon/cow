from subprocess import DEVNULL, PIPE, STDOUT, run

from cow.paths import PathsProvider


class Host:
    def __init__(self, paths_provider: PathsProvider) -> None:
        self._paths_provider = paths_provider

    def run(self, args: list[str], **kwargs):
        if "stdout" in kwargs:
            return run(args, stderr=STDOUT, stdin=DEVNULL, check=True, **kwargs)
        else:
            with open(self._paths_provider.worker_logs, "a", buffering=1) as output:
                return run(
                    args,
                    stdout=output,
                    stderr=STDOUT,
                    stdin=DEVNULL,
                    check=True,
                    **kwargs
                )

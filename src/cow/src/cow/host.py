from subprocess import DEVNULL, PIPE, STDOUT, run


class Host:
    def run(args: list[str], **kwargs):
        result = run(
            args, stderr=STDOUT, stdout=PIPE, stdin=DEVNULL, text=True, **kwargs
        )
        return result.stdout

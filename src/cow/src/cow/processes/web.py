from os import getpid, makedirs
from os.path import join
from contextlib import redirect_stdout, redirect_stderr

from gunicorn.app.base import BaseApplication

from cow.web.app import app
from cow.di import paths_provider


# https://docs.gunicorn.org/en/21.2.0/custom.html#custom-application
class GunicornApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def start_web():
    pid = str(getpid())
    makedirs(paths_provider.logs, exist_ok=True)
    with open(paths_provider.web_logs, "a", buffering=1) as output:
        with redirect_stdout(output):
            with redirect_stderr(output):
                print(f"================== Started web. PID: {pid}")
                options = {
                    "bind": "%s:%s" % ("0.0.0.0", "80"),
                    "workers": 1,
                }
                GunicornApplication(app, options).run()

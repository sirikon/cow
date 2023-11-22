from gunicorn.app.base import BaseApplication

from cow.web.app import app


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
    options = {
        "bind": "%s:%s" % ("0.0.0.0", "80"),
        "workers": 1,
    }
    GunicornApplication(app, options).run()

import tomllib
import os


class ConfigLoader:

    def __init__(self, path="config.toml"):
        self.path = path
        self.config = self.load()

    def load(self):
        if not os.path.exists(self.path):
            return {}

        with open(self.path, "rb") as f:
            return tomllib.load(f)

    def section(self, name):
        return self.config.get(name, {})
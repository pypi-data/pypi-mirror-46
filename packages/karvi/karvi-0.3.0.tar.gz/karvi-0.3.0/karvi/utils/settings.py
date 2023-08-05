import toml
from os import getenv
from karvi.utils.path import Path


class Settings:
    def __init__(self, path=None, mode=None):
        if path:
            if isinstance(path, Path):
                self.__path = path
            elif isinstance(path, str):
                self.__path = Path(path)
            else:
                raise Exception("Parameter 'path' must be a 'String' or 'Path'")

            self.__settings = toml.load(str(self.__path))

    def get(self, key, default=None):
        env = getenv(key, default)
        toml = self.__settings.get(key, default)
        if env:
            return env
        return toml

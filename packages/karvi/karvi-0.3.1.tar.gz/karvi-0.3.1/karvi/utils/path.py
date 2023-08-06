from os.path import isfile, isdir, abspath, join, dirname, exists
from os import PathLike


class Path(PathLike):
    def __init__(self, path):
        self.__path = path

    def is_file(self):
        return isfile(self.__path)

    def is_dir(self):
        return isdir(self.__path)

    def dirname(self):
        if self.is_dir:
            return self.__path
        else:
            return dirname(self.__path)

    def join(self, path):
        newpath = abspath(join(self.__path, path))
        np = Path(newpath)
        if np.exists():
            return np
        else:
            raise Exception('Path "{}" doesn\'t exists'.format(newpath))

    def back(self, count=1):
        newpath = self
        if count >= 1:
            for i in range(count):
                try:
                    newpath = newpath.join("..")
                except Exception as e:
                    raise e
            return newpath
        else:
            pass

    def exists(self):
        return exists(self.__path)

    def __str__(self):
        return self.__path

    def __fspath__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__path == other.__path

    def __neq__(self, other):
        return not self.__eq__(other)

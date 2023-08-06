name = "karvi"
__version__ = "0.3.1"


def get_templates_dir():
    import os

    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/")
    return templates_dir


def get_version():
    return __version__

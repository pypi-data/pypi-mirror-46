from setuptools import setup, find_packages
from karvi import get_version


NAME = "karvi"
VERSION = get_version()
AUTHOR = "Facundo Arano"
AUTHOR_EMAIL = "aranofacundo@gmail.com"
DESCRIPTION = "A small package with custom resources for Django projects."
URL = "https://gitlab.com/aranofacundo/karvi"
REQUIRES_PYTHON = ">=3.6.0"
PACKAGES_REQUIRED = ["django~=2.0", "django-recaptcha~=1.4.0", "django-environ~=0.4.5"]

try:
    with open("README.md", "r") as fh:
        LONG_DESCRIPTION = fh.read()
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "log", "log.*", "*.log", "*.log.*"]),
    install_requires=PACKAGES_REQUIRED,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Django :: 2.0",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)

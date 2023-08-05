import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools import find_packages

from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.install_scripts import install_scripts

here = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = "quick-start"
DESCRIPTION = "My short description for my project."
URL = "http://github.com/andreztz/quick-start"
EMAIL = "andreztz@gmail.com"
AUTHOR = "André Pereira dos Santos"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.0.dev4"


class PostInstallScriptCommand(install_scripts):
    def run(self):
        print("*" * 80)

        install_scripts.run(self)

        from appdirs import user_data_dir
        from appdirs import user_config_dir

        user_data = Path(user_data_dir())
        user_config = Path(user_config_dir())

        user_data = user_data / NAME
        user_config = user_config / NAME

        if not user_data.is_dir():
            user_data.mkdir()
            shutil.copytree("data", user_data / "data")

        if not user_config.is_dir():
            user_config.mkdir()
            shutil.copy("config.ini", user_config)
        print("Installing sources to {} ".format(Path.home()))
        print("*" * 80)


class PostInstallCommand(install):
    def run(self):
        install.run(self)


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)


def readme():
    with open("README.md") as f:
        return f.read()


def required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


package = {
    "name": "quick-start",
    "version": VERSION,
    "description": DESCRIPTION,
    "long_description": readme(),
    "long_description_content_type": "text/markdown",
    "keywords": "quick start project",
    "author": AUTHOR,
    "author_email": EMAIL,
    "url": URL,
    "license": "MIT",
    "packages": find_packages(),
    "install_requires": required(),
    # "include_package_data": True,
    "entry_points": {"console_scripts": ["pyinit=src.__main__:main"]},
    "python_requires": REQUIRES_PYTHON,
    "classifiers": [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    "cmdclass": {
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
        "install_scripts": PostInstallScriptCommand,
    },
}


setup(**package)

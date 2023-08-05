import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools import find_packages

from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install
from setuptools.command.install_scripts import install_scripts

here = os.path.abspath(os.path.dirname(__file__))

NAME = "quick-start"
DESCRIPTION = "My short description for my project."
URL = "http://github.com/andreztz/quick-start"
EMAIL = "andreztz@gmail.com"
AUTHOR = "André Pereira dos Santos"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.0.dev9"


# def wizard():
#     from appdirs import user_data_dir
#     from appdirs import user_config_dir
#
#     user_data = Path(user_data_dir())
#     user_config = Path(user_config_dir())
#
#     user_data = user_data / NAME
#     user_config = user_config / NAME
#
#     print("*" * 80)
#     if not user_data.is_dir():
#         user_data.mkdir()
#         shutil.copytree("data", user_data / "data")
#
#     if not user_config.is_dir():
#         user_config.mkdir()
#         shutil.copy("config.ini", user_config)
#     print("Installing sources to {} ".format(Path.home()))
#     print("*" * 80)


class PostInstallScriptCommand(install_scripts):
    def run(self):
        install_scripts.run(self)


class PostEggInfoCommand(egg_info):
    def run(self):
        egg_info.run(self)


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        install.run(self)


def readme():
    with open(os.path.join(here, "README.md")) as f:
        return f.read()


def required():
    with open(os.path.join(here, "requirements.txt")) as f:
        return f.read().splitlines()


package = {
    "name": NAME,
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
    "entry_points": {
        "console_scripts": ["pyinit=quickstart.__main__:main"],
        # "setuptools.installation": [
        #     "eggsecutable=quickstart.quickstart_installer:wizard"
        # ],
    },
    "python_requires": REQUIRES_PYTHON,
    "scripts": [os.path.join(here, "quickstart/quickstart_installer.py")],
    "classifiers": [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    "cmdclass": {
        "develop": PostDevelopCommand,
        "egg_info": PostEggInfoCommand,
        "install": PostInstallCommand,
        "install_scripts": PostInstallScriptCommand,
    },
}


setup(**package)

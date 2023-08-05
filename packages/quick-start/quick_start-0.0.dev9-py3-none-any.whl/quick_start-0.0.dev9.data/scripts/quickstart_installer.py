#!python

import shutil
from pathlib import Path

from appdirs import user_data_dir
from appdirs import user_config_dir


NAME = "quick-start"


def wizard():

    user_data = Path(user_data_dir())
    user_config = Path(user_config_dir())

    user_data = user_data / NAME
    user_config = user_config / NAME

    print("*" * 80)
    if not user_data.is_dir():
        user_data.mkdir()
        shutil.copytree("data", user_data / "data")

    if not user_config.is_dir():
        user_config.mkdir()
        shutil.copy("config.ini", user_config)
    print("Installing sources to {} ".format(Path.home()))
    print("*" * 80)


wizard()

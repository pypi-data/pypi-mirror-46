import sys
import zipfile

import click

from src.config import current_work_directory
from src.config import sample_zip


def wizard():
    pass


def unzip_file(file, extract_to):
    with zipfile.ZipFile(file, "r") as zip:
        zip.extractall(extract_to)


def main():
    @click.command()
    @click.argument("project_name", nargs=1, default="sample")
    def add(project_name):
        path = current_work_directory / project_name
        unzip_file(sample_zip, path)

    add()


if __name__ == "__main__":
    main()

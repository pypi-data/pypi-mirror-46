# Arquivo responsável por gerenciar as configurações do usuário.

from pathlib import Path

from appdirs import user_config_dir
from appdirs import user_data_dir


base_dir = Path(__file__).parent
project_root = base_dir.parent
config_ini = project_root / "config.ini"
current_work_directory = Path.cwd()
sample_zip = project_root.joinpath('data/sample.zip')

if __name__ == '__main__':
    print(base_dir)
    print(project_root)
    print(sample_zip)

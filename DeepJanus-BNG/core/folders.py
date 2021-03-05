import os
from pathlib import Path
from datetime import datetime

class Folders:
    def __init__(self, lib_folder: str):
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        self.lib: Path = Path(lib_folder).resolve()
        self.root: Path = self.lib.joinpath('..').resolve()
        self.data: Path = self.root.joinpath('data').absolute()
        self.log_ini: Path = self.data.joinpath('log.ini').absolute()
        self.member_seeds: Path = self.data.joinpath('member_seeds').absolute()
        self.experiments: Path = self.data.joinpath('experiments_'+str(now)).absolute()
        self.simulations: Path = self.data.joinpath('simulations_'+str(now)).absolute()
        self.trained_models_colab: Path = self.data.joinpath('trained_models_colab').absolute()


folders: Folders = Folders(os.path.dirname(__file__))

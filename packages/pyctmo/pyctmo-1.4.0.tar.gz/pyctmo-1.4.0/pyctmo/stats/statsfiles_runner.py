import subprocess
from pathlib import Path
import os
from statsfiles import statsfiles

class StatsFileRunner:

    def __init__(self):
        pass

    def run_statsfiles(self, folderpath:str, startiter:int):
        os.chdir(folderpath)
        statsfiles.run_statsfiles(startiter)
        # subprocess.run(
        #     f"{StatsFileRunner.PYTHON_INTERPRETER} -m statsfiles --cdh {startiter} ", shell=True
        # )

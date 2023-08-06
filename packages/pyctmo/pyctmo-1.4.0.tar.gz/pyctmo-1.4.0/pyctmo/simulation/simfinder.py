import os
from typing import List
from copy import deepcopy
class SimFinder:

    def __init__(self, root_folder=os.getcwd()):
        self._root_folder:str = root_folder
        self._sim_folders:List[str] = []
        self._get_sim_folders()

    def _get_sim_folders(self)->None:

        for tt in os.walk(self._root_folder):
            base_folder = tt[0]
            folders = tt[1]

            for (ii, folder) in enumerate(deepcopy(folders)):
                folders[ii] = os.path.join(base_folder, folder)

            folders = list(map(os.path.abspath, folders))
            for folder in folders:
                # print(f"folder = {folder}")
                if self.is_sim_foler(folder):
                    self._sim_folders.append(folder)

    @staticmethod
    def is_sim_foler(folder:str) -> bool:

        files = os.listdir(folder)
        # print(f"files = {files}")
        # print("hybNextUp.dat" in files)
        return ("greenUp.dat" in files and "Obs.json" in files)


    @property
    def sim_folders(self)->List[str]:
        return self._sim_folders

import numpy as np
import math
import os


class StatsLogic:
    INITIAL_SIM_LENGTH: int = 100
    INITIAL_SAMPLE_SIZE: int = 30
    INITIAL_SAMPLE_RATIO: float = 0.33333333
    MAX_SAMPLE_RATIO: float = 0.9
    ERROR: int = -999
    INCREMENT: int = 10
    WEIGHT_SLOPE: float = 0.50
    WEIGHT_STD: float = 1.0

    def __init__(self, foldername: str, is_simplelogic=True):

        assert StatsLogic.INITIAL_SIM_LENGTH > StatsLogic.INITIAL_SAMPLE_SIZE/StatsLogic.INITIAL_SAMPLE_RATIO

        os.chdir(foldername)
        self._foldername: str = foldername
        self._is_simplelogic = is_simplelogic

        self._lastiter: int = -1
        with open("n.dat") as fin:
            self._lastiter = len(fin.readlines()) - 1
        print(f"self._lastiter = {self._lastiter}")
        print(f"foldername = {foldername}")

        # Get the self-energies
        self._selfenergies = []

        for ii in range(1, self._lastiter + 1):
            selfenergy_file: str = "selfUp" + str(ii) + ".dat"
            self._selfenergies.append(np.loadtxt(selfenergy_file))

        # # The self-energyies, each iteration is in the first index
        # self._selfenergy_cube: np.ndarray = np.zeros(
        #     (
        #         self._lastiter,
        #         self._selfenergies[0].shape[0],
        #         self._selfenergies[0].shape[1],
        #     )
        # )
        # for ii in range(self._lastiter):
        #     self._selfenergy_cube[ii] = self._selfenergies[ii]

        self._sample_size: int = StatsLogic.ERROR
        self._sample_size = self._get_sample_size()
        self._startiter = self._lastiter - self._sample_size
        assert (
            self._startiter
            > self._startiter - StatsLogic.MAX_SAMPLE_RATIO * self._lastiter
        )

    def _get_sample_size(self):

        if self._is_simplelogic:
            if self._lastiter < StatsLogic.INITIAL_SIM_LENGTH:
                return math.floor(
                    min(
                        StatsLogic.INITIAL_SAMPLE_SIZE,
                        StatsLogic.INITIAL_SAMPLE_RATIO * self._lastiter,
                    )
                )
            else:
                return math.floor(max(StatsLogic.INITIAL_SAMPLE_SIZE,  StatsLogic.INITIAL_SAMPLE_RATIO * self._lastiter))
        else:
            raise NotImplementedError("Only simple logic error is implemented for now.")

        # slopes = []
        # stds = []
        # if self._lastiter < StatsLogic.INITIAL_SIM_LENGTH:
        #     sample_size = math.floor(
        #         min(
        #             StatsLogic.INITIAL_SAMPLE_SIZE,
        #             StatsLogic.INITIAL_SAMPLE_RATIO * self._lastiter,
        #         )
        #     )
        #     return sample_size
        # else:
        #     sample_size: int = StatsLogic.INITIAL_SAMPLE_SIZE
        #     sample_size_list: List[int] = []
        #
        #     while sample_size < StatsLogic.MAX_SAMPLE_RATIO * self._lastiter:
        #         iterstart: int = self._lastiter - sample_size
        #         sample_size_list.append(sample_size)
        #
        #         # For iterations from iterstart to last iteration, the first matsubara frequency
        #         # of the first self-energy imaginary part
        #         values = self._selfenergy_cube[iterstart:, 0, 2]
        #         slope = np.polyfit(np.arange(values.shape[0]), values, 1)[0]
        #         std = np.std(values)
        #         slopes.append(slope)
        #         stds.append(std)
        #         sample_size += StatsLogic.INCREMENT
        #
        #     scores = []
        #     for ii in range(len(stds)):
        #         scores.append(self.get_score(slopes[ii], stds[ii]))
        #
        #     best_index = np.where(scores == np.min(scores))[0][0]
        #     print(f"scores = {scores}")
        #     print(f"best_index = {best_index}")
        #     return sample_size_list[best_index]

    def get_score(self, slope: float, std: float):
        return self.WEIGHT_SLOPE * abs(slope) + self.WEIGHT_STD * std

    @property
    def startiter(self):
        return self._startiter

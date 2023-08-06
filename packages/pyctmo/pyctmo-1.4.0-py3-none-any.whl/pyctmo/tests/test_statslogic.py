from pyctmo.stats.statslogic import StatsLogic
import unittest
import warnings
import os
import inspect

class TestStatsLogic(unittest.TestCase):
    CURR_DIR: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    FOLDER_PATH: str =  os.path.join(CURR_DIR, "data/tp04_DCA_3x2/n1/beta12/U5.75")
    FOLDER_PATH_LEGACY: str = os.path.join(CURR_DIR, "data/DCA_4x4/U5.7_n0.99")

    def test_simple_logic(self):
        statslogic = StatsLogic(TestStatsLogic.FOLDER_PATH)
        warnings.warn("TEST not implemented, test with a dmft simulation of at least 300 iterations also.")



if __name__ == "__main__":
    unittest.main()



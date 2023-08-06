from pyctmo.simulation.simfinder import SimFinder
import unittest
import os
import inspect

class TestSimFinder(unittest.TestCase):

    CURR_DIR: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    def test_init(self):
        sim_finder = SimFinder()
        sim_folders = sim_finder.sim_folders
        print(f"sim_folders = {sim_folders}")
        self.assertEqual(len(sim_folders), 4)

        self.assertTrue(
            os.path.join(TestSimFinder.CURR_DIR, "data/tp04_DCA_3x2/n1/beta12/U5.75")
            in sim_folders
        )
        self.assertTrue(
            os.path.join(TestSimFinder.CURR_DIR,"data/tp04_DCA_3x2/n1/beta12/U6.00")
            in sim_folders
        )
        self.assertTrue(
            os.path.join(TestSimFinder.CURR_DIR, "data/DCA_4x4/U5.7_n0.99")
            in sim_folders
        )



if __name__ == "__main__":
    unittest.main()

from pyctmo.utils.configs_unpacker import ConfigsUnpacker
import unittest
import os
import inspect
import warnings
import json
import numpy as np


class TestConfigsUnpacker(unittest.TestCase):

    CURR_DIR: str = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    DIR_DMFT: str = os.path.join(CURR_DIR, "data/dmft_U5_b10_mu2.5")

    def test_init(self):

        config_unpacker = ConfigsUnpacker(TestConfigsUnpacker.DIR_DMFT)
        batch_files = config_unpacker.batch_files
        batch_files.sort()
        good_batch_files = [
            "configs_0_ctmo.bin",
            "configs_1_ctmo.bin",
            "configs_2_ctmo.bin",
            "configs_3_ctmo.bin",
            "configs_4_ctmo.bin",
            "configs_5_ctmo.bin",
        ]
        good_batch_files.sort()
        self.assertEqual(batch_files, good_batch_files)
        warnings.warn(
            """Continue testing, get the batch compressed, uncompress it and 
                      make sure that it is the same as the saved json."""
        )

        json_file = os.path.join(TestConfigsUnpacker.DIR_DMFT, "batchConfig11.json")
        with open(json_file) as fin:
            jj_batch = json.load(fin)

        batch = config_unpacker.batches[11]
        batch_uncompressed = batch
        self.assertEqual(batch_uncompressed, batch)
        np.testing.assert_allclose(batch[b"431"][b"taus"], jj_batch["431"]["taus"])
        np.testing.assert_allclose(
            batch[b"431"][b"auxSpins"], jj_batch["431"]["auxSpins"]
        )
        np.testing.assert_allclose(batch[b"431"][b"sign"], jj_batch["431"]["sign"])
        np.testing.assert_allclose(
            batch[b"431"][b"logDeterminant"], jj_batch["431"]["logDeterminant"]
        )


if __name__ == "__main__":
    unittest.main()

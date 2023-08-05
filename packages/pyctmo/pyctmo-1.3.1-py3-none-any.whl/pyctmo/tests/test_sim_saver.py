from pyctmo.simulation.simsaver import SimSaver
from pyctmo.db.postgresqldriver import PgSqlDriver
import unittest
import numpy as np
import os
import json
import inspect
from pyctmo.utils.configs_unpacker import ConfigsUnpacker
import msgpack
import zlib
import snappy

class TestSimSaver(unittest.TestCase):
    CURR_DIR: str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    FOLDER_PATH: str = os.path.join(CURR_DIR, "data/tp04_DCA_3x2/n1/beta12/U5.75")
    FOLDER_PATH_2: str = os.path.join(CURR_DIR, "data/tp04_DCA_3x2/n1/beta12/U6.00")

    FOLDER_PATH_LEGACY: str = os.path.join(CURR_DIR, "data/DCA_4x4/U5.7_n0.99")
    FOLDER_DMFT: str = os.path.join(CURR_DIR, "data/dmft_U5_b10_mu2.5")

    @classmethod
    def setUpClass(cls):
        pg = PgSqlDriver()
        sqlcmd = f"TRUNCATE test__simulations CASCADE;"
        pg.execute(sqlcmd, commit=True)

    def test_new_version(self):

        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH)
        self.assertEqual(sim_saver.version, sim_saver.DEFAULT_CTMO_VERSION)
        self.assertEqual(sim_saver.lastiter, 87)
        self.assertEqual(sim_saver.modelname, "Triangle3x2_DCA")
        simple_params = SimSaver.SimpleParams(
            U=5.75,
            mu=2.88,
            beta=12.0,
            UPrime=0.0,
            J_H=0.0,
            nOrb=1,
            gPhonon=0.0,
            w0Phonon=0.0,
        )

        np.testing.assert_allclose(simple_params, sim_saver.simple_params)

    def test_new_version_save(self):
        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH_2)
        sim_saver.save_sim()
        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH)
        sim_saver.save_sim()

    def test_sim(self):
        TestSimSaver.setUpClass()

        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH_2)
        sim_saver.save_sim()
        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH)
        sim_saver.save_sim()

        pgdb = PgSqlDriver()

        sqlcmd = f"SELECT * FROM test__simulations WHERE model_name = 'Triangle3x2_DCA' ORDER  BY id DESC;"
        simple_params_list = pgdb.fetchall(sqlcmd)
        self.assertTrue(len(simple_params_list), 1)
        simple_params = simple_params_list[0]

        self.assertAlmostEqual(simple_params["model_name"], "Triangle3x2_DCA")
        self.assertAlmostEqual(simple_params["U"], 5.75)
        self.assertAlmostEqual(simple_params["mu"], 2.88)
        self.assertAlmostEqual(simple_params["beta"], 12.0)
        self.assertAlmostEqual(simple_params["J_H"], 0.0)
        self.assertAlmostEqual(simple_params["nOrb"], 1.0)
        self.assertAlmostEqual(simple_params["gPhonon"], 0.0)
        self.assertAlmostEqual(simple_params["w0Phonon"], 0.0)
        self.assertAlmostEqual(simple_params["ctmo_version"], "2.0.0")

        with open(os.path.join(TestSimSaver.FOLDER_PATH, "params87.json")) as fin:
            params = json.load(fin)

        self.assertTrue(json.dumps(params) == json.dumps(simple_params["params"]))

    def test_obs_scalar(self):
        TestSimSaver.setUpClass()

        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH_2)
        sim_saver.save_sim()
        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH)
        sim_saver.save_sim()

        pgdb = PgSqlDriver()

        for ss in ["n", "k", "sign", "docc"]:
            with open(os.path.join(TestSimSaver.FOLDER_PATH, ss + ".dat")) as fin:
                ss_dat = fin.read()

            sqlcmd = f"""SELECT obs.{ss+'_dat'} FROM test__obs__scalar as obs 
                                                    INNER JOIN test__simulations  AS sim  ON obs.simulation_id = sim.id
                                                    WHERE sim."U" BETWEEN 5.749 AND 5.751"""
            result = pgdb.fetchone(sqlcmd)
            self.assertEqual(result[ss + "_dat"], ss_dat)

    def test_cubes(self):
        TestSimSaver.setUpClass()

        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH_2)
        sim_saver.save_sim()
        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH)
        sim_saver.save_sim()

        pgdb = PgSqlDriver()

        # for cube_t in ["gf", "hyb", "self"]:
        for ss in ["mean", "std"]:
            sqlcmd = f"SELECT * FROM test__obs__gf ORDER  BY id DESC LIMIT 1;"
            gf_saved = zlib.decompress(pgdb.fetchone(sqlcmd)["gfup_" + ss]).decode(
                "utf-8"
            )
            self.assertTrue(gf_saved == sim_saver.obs_gf["gfup_" + ss])
            with open(
                os.path.join(sim_saver.folderpath, "greenUp_" + ss + ".dat")
            ) as fin:
                gf_read = fin.read()
            self.assertTrue(gf_read == gf_saved)

        self.assertTrue(
            pgdb.fetchone("SELECT * FROM test__obs__gf ORDER  BY id DESC LIMIT 1;")[
                "gfdown_mean"
            ]
            is None
        )
        self.assertTrue(
            pgdb.fetchone("SELECT * FROM test__obs__gf ORDER  BY id DESC LIMIT 1;")[
                "gfdown_std"
            ]
            is None
        )

        with open(os.path.join(sim_saver.folderpath, "selfUp_mean.dat")) as fin:
            self_read = fin.read()

        sqlcmd = f"SELECT * FROM test__obs__self ORDER  BY id DESC LIMIT 1;"
        self_saved = zlib.decompress(pgdb.fetchone(sqlcmd)["selfup_mean"]).decode(
                "utf-8"
            )
        self.assertEqual(self_read, self_saved)

        with open(os.path.join(sim_saver.folderpath, "hybUp_mean.dat")) as fin:
            hyb_read = fin.read()

        sqlcmd = f"SELECT * FROM test__obs__hyb ORDER  BY id DESC LIMIT 1;"
        hyb_saved = zlib.decompress(pgdb.fetchone(sqlcmd)["hybup_mean"]).decode(
                "utf-8"
            )
        self.assertEqual(hyb_read, hyb_saved)

    def test_save_configs(self):
        sim_saver = SimSaver(TestSimSaver.FOLDER_DMFT)
        sim_saver.save_sim()

        config_unpacker = ConfigsUnpacker(TestSimSaver.FOLDER_DMFT)
        batch = config_unpacker.batches[11]

        pgdb = PgSqlDriver()
        sqlcmd = f"SELECT * FROM test__configs__batches ORDER BY id ASC LIMIT 15;"
        batch_saved = msgpack.unpackb(snappy.decompress(pgdb.fetchall(sqlcmd)[11]["batch"]))
        self.assertEqual(batch, batch_saved)






    def test_legacy_version(self):

        sim_saver = SimSaver(TestSimSaver.FOLDER_PATH_LEGACY)
        self.assertEqual(sim_saver.version, sim_saver.LEGACY_CTMO_VERSION)
        self.assertEqual(sim_saver.lastiter, 22)
        self.assertEqual(sim_saver.modelname, "Square4x4_DCA")
        simple_params = SimSaver.SimpleParams(
            U=5.7,
            mu=2.75,
            beta=20.0,
            UPrime=0.0,
            J_H=0.0,
            nOrb=1,
            gPhonon=0.0,
            w0Phonon=0.0,
        )

        np.testing.assert_allclose(simple_params, sim_saver.simple_params)


if __name__ == "__main__":
    unittest.main()

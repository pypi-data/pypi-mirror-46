from pyctmo.db import postgresqldriver
from pyctmo.utils.simplelog import SimpleLog
from pyctmo.utils.configs_unpacker import ConfigsUnpacker

import os
import json
from typing import Dict
import numpy as np
from collections import namedtuple
import zlib
import pandas as pd


class SimSaver:

    DEFAULT_CTMO_VERSION: str = "2.0.0"
    LEGACY_CTMO_VERSION: str = "1.0.0"
    SIM_ID_UNDEFINED: int = -9999
    LAST_ITER_UNDEFINED: int = -999
    SCALAR_FILES: Dict[str, str] = {
        "obs_json": "Obs.json",
        "stats_obs": "statsobs.json",
        "n_dat": "n.dat",
        "k_dat": "k.dat",
        "sign_dat": "sign.dat",
        "docc_dat": "docc.dat",
    }

    CUBE_FILES = {
        "gf": {
            "gfup_mean": "greenUp_mean.dat",
            "gfup_std": "greenUp_std.dat",
            "gfdown_mean": "greenDown_mean.dat",
            "gfdown_std": "greenDown_std.dat",
            "conventions": "outPutConvention.dat",
        },
        "hyb": {
            "hybup_mean": "hybUp_mean.dat",
            "hybup_std": "hybUp_std.dat",
            "hybdown_mean": "hybDown_mean.dat",
            "hybdown_std": "hybDown_std.dat",
            "conventions": "outPutConvention.dat",
        },
        "self": {
            "selfup_mean": "selfUp_mean.dat",
            "selfup_std": "selfUp_std.dat",
            "selfdown_mean": "selfDown_mean.dat",
            "selfdown_std": "selfDown_std.dat",
            "conventions": "outPutConvention.dat",
        },
    }

    CONFIGURATION_FILES: Dict[str, str] = dict()

    SimpleParams = namedtuple(
        "SimpleParams",
        ["U", "mu", "beta", "UPrime", "J_H", "nOrb", "gPhonon", "w0Phonon"],
    )

    CTMO_VERSION: str = "2.0.0"

    def __init__(self, sim_folderpath: str, istest=True):
        """ """
        self._istest = istest
        self._sim_folderpath = sim_folderpath
        self._dbdriver = postgresqldriver.PgSqlDriver(cursorclass="DICT")
        folders = [
            ff
            for ff in os.listdir(sim_folderpath)
            if os.path.isdir(os.path.join(sim_folderpath, ff))
            and ff.startswith("Stats")
        ]
        assert len(folders) == 1

        # The Stats folder path
        self._folderpath = os.path.join(sim_folderpath, folders[0])
        os.chdir(self._folderpath)

        self._statsobs: Dict = dict()
        self._simparams: Dict = dict()
        self._modelname: str = ""
        self._lastiter: int = SimSaver.LAST_ITER_UNDEFINED
        self._simpleparams: Dict = dict()

        self._is_already_saved = False
        self._logger = SimpleLog(logger_name="SimSaver")
        self._version = SimSaver.DEFAULT_CTMO_VERSION

        if self._istest:
            self._table_sim: str = "test__simulations"
            self._table_obs_scalar: str = "test__obs__scalar"
            self._table_configs: str = "test__configs__batches"
            self._table_obs_cubes: Dict[str, str] = {
                "gf": "test__obs__gf",
                "hyb": "test__obs__hyb",
                "self": "test__obs__self",
            }
        else:
            self._table_sim: str = "simulations"
            self._table_obs_scalar: str = "obs__scalar"
            self._table_configs: str = "configs__batches"
            self._table_obs_cubes: Dict[str, str] = {
                "gf": "obs__gf",
                "hyb": "obs__hyb",
                "self": "obs__self",
            }

        self._obs_cubes = {"gf": dict(), "hyb": dict(), "self": dict()}
        self._obs_scalar = dict()
        self._sim_id: int = SimSaver.SIM_ID_UNDEFINED
        self._get_simulation()

    @property
    def modelname(self):
        return self._modelname

    @property
    def lastiter(self):
        return self._lastiter

    @property
    def simple_params(self):
        return self._simpleparams

    @property
    def version(self):
        return self._version

    @property
    def obs_gf(self):
        return self._obs_cubes["gf"]

    @property
    def obs_hyb(self):
        return self._obs_cubes["hyb"]

    @property
    def obs_self(self):
        return self._obs_cubes["self"]

    @property
    def folderpath(self):
        return self._folderpath

    def _get_simulation(self)->None:
        os.chdir(self._folderpath)

        try:
            with open("n.dat") as fin:
                self._lastiter = len(fin.readlines()) - 1
                print(f"lastiter = {self._lastiter}")
                print(f"file_path = {self._folderpath}")
            with open("statsobs.json") as fin:
                self._statsobs = json.load(fin)
            with open("params" + str(self._lastiter) + ".json") as fin:
                self._simparams = json.load(fin)

            if "model" in self._simparams:
                self._logger.info(f"ctmo version = {SimSaver.DEFAULT_CTMO_VERSION}")
                self._simpleparams = SimSaver.SimpleParams(
                    U=self._simparams["model"]["U"],
                    mu=self._simparams["model"]["mu"],
                    beta=self._simparams["model"]["beta"],
                    UPrime=self._simparams["model"]["UPrime"],
                    J_H=self._simparams["model"]["J_H"],
                    nOrb=self._simparams["model"]["nOrb"],
                    gPhonon=self._simparams["model"]["gPhonon"],
                    w0Phonon=self._simparams["model"]["w0Phonon"],
                )
                self._modelname = [
                    ss for ss in os.listdir(os.getcwd()) if ".model" in ss
                ][0]
                self._modelname = self._modelname.split(".")[0]
            else:
                self._logger.info(f"ctmo version = {SimSaver.LEGACY_CTMO_VERSION}")
                self._version = SimSaver.LEGACY_CTMO_VERSION
                self._simpleparams = SimSaver.SimpleParams(
                    U=self._simparams["U"],
                    mu=self._simparams["mu"],
                    beta=self._simparams["beta"],
                    UPrime=0.0,
                    J_H=0.0,
                    nOrb=1,
                    gPhonon=0.0,
                    w0Phonon=0.0,
                )
                self._modelname = self._simparams["modelType"]

        except (IOError, IndexError) as err:
            self._logger.error(
                f"Warning, simulation not found for file {self._folderpath}"
            )
            raise

    def _verify_if_saved(self)->bool:
        # Get U, norb, etc and make sure that there is no other simulation like that and if there is
        # then lastiter should be bigger than the saved sim to overwrite.
        sqlcmd = f"""
                 SELECT * FROM {self._table_sim}   
                 """
        simulations = self._dbdriver.fetchall(sqlcmd)
        sqlcmd = f"""
                 SELECT * FROM {self._table_obs_scalar}
                 """
        nb_simulations: int = len(simulations)
        # if self._istest:
        #     assert nb_simulations == 3

        sim_ids = np.zeros(nb_simulations, dtype=np.int64)
        model_names = np.zeros(nb_simulations, dtype=np.string_)
        simple_params = np.zeros((len(simulations), 8), dtype=np.float64)
        sim_params = []
        for (ii, dd) in enumerate(simulations):
            sim_ids[ii] = dd["id"]
            model_names[ii] = dd["model_name"]
            simple_params[ii] = SimSaver.SimpleParams(
                U=dd["U"],
                mu=dd["mu"],
                beta=dd["beta"],
                UPrime=dd["UPrime"],
                J_H=dd["J_H"],
                nOrb=dd["nOrb"],
                gPhonon=dd["gPhonon"],
                w0Phonon=dd["w0Phonon"],
            )
            sim_params.append(dd["params"])
            if np.allclose(simple_params[ii], self._simpleparams):
                self._is_already_saved = True
                break

        if self._is_already_saved:
            if self._version == SimSaver.LEGACY_CTMO_VERSION:
                self._logger.info(
                    "Legacy version, not checking further, not saving simulation."
                )
            else:
                self._logger.info(
                    "Simulation, seems already saved when checking simple params, Checking tParameters. 00"
                )
                self._is_already_saved = False
                series_curr_tparams_00 = pd.Series(
                    self._simparams["model"]["tParameters"]["00"]
                )
                for (jj, (sim_id, params)) in enumerate(zip(sim_ids, sim_params)):
                    if not "model" in params.keys():
                        continue
                    series_t_params00 = pd.Series(params["model"]["tParameters"]["00"])
                    if series_curr_tparams_00.equals(series_t_params00) and np.allclose(
                        simple_params[jj], self._simpleparams
                    ):
                        self._is_already_saved = True
                        self._logger.warning(
                            f"Warning, duplicate simulation, not re-saving the simulation at {self._folderpath} \n"
                            f"\t with id {sim_id}"
                        )
                        break

        return self._is_already_saved

    def save_sim(self)->None:
        if not self._verify_if_saved():

            # Save the simulation
            sqlcmd = f"""
                        INSERT INTO {self._table_sim}(model_name, "U", mu, beta, "UPrime", "J_H", 
                        "nOrb", "gPhonon", "w0Phonon",  ctmo_version, params) 
                        VALUES('{self._modelname}', '{self._simpleparams.U}', '{self._simpleparams.mu}', 
                               '{self._simpleparams.beta}', '{self._simpleparams.UPrime}',  '{self._simpleparams.J_H}',
                               '{self._simpleparams.nOrb}', '{self._simpleparams.gPhonon}', '{self._simpleparams.w0Phonon}',
                               '{self._version}', '{json.dumps(self._simparams)}') ;
                        """
            self._dbdriver.execute(sqlcmd)
            self._sim_id: int = self._dbdriver.fetchone(
                f"SELECT MAX(id) FROM {self._table_sim};"
            )["max"]

            try:
                self._save_obs_scalar()
                self._save_cubes()
                self._save_configs()
                self._dbdriver.commit()
            except FileNotFoundError as err:
                raise

    def _save_obs_scalar(self)->None:
        # Save the scalar files

        obs_scalar = dict()  # namedtuple("ObsScalar", SimSaver.SCALAR_FILES.keys())
        for (key, value) in SimSaver.SCALAR_FILES.items():
            with open(value) as fin:
                obs_scalar[key] = fin.read()
        sqlcmd = f"""
                     INSERT INTO {self._table_obs_scalar}(simulation_id, obs_json, stats_obs, n_dat, k_dat,
                                                          sign_dat, docc_dat)
                    VALUES('{self._sim_id}', '{obs_scalar["obs_json"]}', '{obs_scalar["stats_obs"]}', 
                           '{obs_scalar["n_dat"]}',
                           '{obs_scalar["k_dat"]}', '{obs_scalar["sign_dat"]}', '{obs_scalar["docc_dat"]}')
                                """
        self._dbdriver.execute(sqlcmd)

    def _save_cubes(self)->None:
        """ Save cubes: gf, hyb and Self-energies"""
        # save the cube
        for (cube_t, files_dict) in SimSaver.CUBE_FILES.items():
            for (key, value) in files_dict.items():
                try:
                    with open(value) as fin:
                        self._obs_cubes[cube_t][key] = fin.read()
                except FileNotFoundError as err:
                    self._logger.info(f"{err}")
                    self._obs_cubes[cube_t][key] = None

            sqlcmd = f"""
                                    INSERT INTO {self._table_obs_cubes[cube_t]}(simulation_id, conventions, {cube_t + 'up_mean'}, {cube_t + 'up_std'}, {cube_t + 'down_mean'}, {cube_t + 'down_std'})
                                    VALUES('{self._sim_id}', '{self._obs_cubes[cube_t]["conventions"]}',
                                           %s, %s, %s, %s);
                                    """
            cubeup_mean = zlib.compress(
                self._obs_cubes[cube_t][cube_t + "up_mean"].encode("utf-8")
            )
            cubeup_std = zlib.compress(
                self._obs_cubes[cube_t][cube_t + "up_std"].encode("utf-8")
            )
            cubedown_mean = (
                zlib.compress(
                    self._obs_cubes[cube_t][cube_t + "down_mean"].encode("utf-8")
                )
                if self._obs_cubes[cube_t][cube_t + "down_mean"]
                else None
            )
            cubedown_std = (
                zlib.compress(
                    self._obs_cubes[cube_t][cube_t + "down_std"].encode("utf-8")
                )
                if self._obs_cubes[cube_t][cube_t + "down_std"]
                else None
            )

            self._dbdriver.execute(
                sqlcmd, params=[cubeup_mean, cubeup_std, cubedown_mean, cubedown_std]
            )

    def _save_configs(self)->None:
        parent_dir = os.path.abspath(os.path.join(self._folderpath, os.path.pardir))
        config_unpacker = ConfigsUnpacker(parent_dir)
        batches_compressed = config_unpacker.batches_compressed

        for batch_c in batches_compressed:
            sqlcmd = f"""
                     INSERT INTO {self._table_configs}(simulation_id, batch) VALUES (%(simulation_id)s, %(batch_c)s)
                      """

            self._dbdriver.execute(
                sqlcmd, params={"simulation_id": self._sim_id, "batch_c": batch_c}
            )

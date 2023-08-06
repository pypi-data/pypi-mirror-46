from .postgresqldriver import PgSqlDriver
from ..utils.simplelog import SimpleLog


from typing import List, Dict
import configparser
import os
import pathlib
import json
import snappy
import msgpack
from tqdm import tqdm
import numpy as np
import random
from copy import deepcopy
from keras.utils import Sequence


class DataParser(Sequence):
    """
    A simple class that parses and helps with CTMO C++ generated data.
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(pathlib.Path.home(), ".pyctmo/pyctmo.cnf"))
        self._cache_path = config["DATAPARSER"]["cache_directory"]
        self._logger = SimpleLog("DataParser")

        self._simulations_id: List[int] = []
        self._simulations_params: List[Dict] = []
        self._trian_generator_ready = False

        self.INPUT_SHAPE: int = 400
        self.NUM_FILES_PER_BATCH: int = 10

        self.VALIDATION_RATIO: float = 0.01
        self.TEST_RATIO: float = 0.01

        self._test_files: List[str] = []
        self._train_files: List[str] = []
        self._val_files: List[str] = []

        self._validation_data: (np.array(), np.array()) = None
        self._test_data: (np.array(), np.array()) = None

        self._prepare_trian_generator()

    @property
    def get_num_train_batches(self):
        return int(len(self._train_files) / self.NUM_FILES_PER_BATCH)

    def __len__(self):
        return self.get_num_train_batches

    @property
    def validation_data(self):
        if not self._validation_data:
            self._get_validation_data()
        return self._validation_data

    @property
    def test_data(self):
        if not self._test_data:
            self._get_test_data()
        return self._test_data

    @property
    def simulations_id(self) -> List[int]:
        """
        Get a list of the simulation unique id. Each element of the list
        is an id (int).
        Parameters
        ----------
        Returns: List[Int]
            The simulation ids
        -------
        """
        if not self._simulations_id:
            self._get_simulations_id()
        return self._simulations_id

    @property
    def simulations_params(self) -> List[Dict]:
        """
        Get a list of the simulation parameters. Each element of the list
        is a dictionary.
        Parameters
        ----------
        Returns: List[Dict]
            The simulation parameters
        -------

        Example usages:
        ---------------
        simulation_params = simulation_params
        keys_parmas = simulation_params[0].keys()
        """
        if not self._simulations_params:
            self._get_simulations_params()
        return self._simulations_params

    def build_cache(self, only_dmft: bool = True, delete_old: bool = False) -> None:

        if not os.path.isdir(self._cache_path):
            os.mkdir(self._cache_path)
            os.chdir(self._cache_path)
        else:
            self._logger.warning(
                f"""Not building cache again, the cache directory, {self._cache_path} ,
                                 alredy exists"""
            )

        # 0.) get the simulations
        pgd = PgSqlDriver()
        result = None
        if only_dmft:
            result = pgd.fetchall(
                "SELECT id FROM simulations WHERE model_name ='SIAM_Square' "
            )
        else:
            result = pgd.fetchall("SELECT id FROM simulations")

        sim_ids: List[int] = []
        for row in result:
            sim_ids.append(row["id"])

        for sim_id in tqdm(sim_ids):
            dir_path: str = os.path.join(self._cache_path, f"simulation_{sim_id}")
            if os.path.isdir(dir_path):
                if not delete_old:
                    continue
                else:
                    raise NotImplementedError
                    # shutil.rmtree(dir_path)
                    # os.mkdir(dir_path)
            params = pgd.fetchone(
                "SELECT params FROM simulations WHERE id=%s", params=(sim_id,)
            )
            os.mkdir(dir_path)
            with open(os.path.join(dir_path, "params.json"), "w") as fout:
                json.dump(params, fout, indent=4)

            batches_ids: List[int] = pgd.fetchall(
                "SELECT id from configs__batches WHERE simulation_id=%s",
                params=(sim_id,),
            )

            for (jj, row) in enumerate(batches_ids):
                batch: bytes = pgd.fetchone(
                    "SELECT batch from configs__batches WHERE id=%s",
                    params=(row["id"],),
                )["batch"]
                filename: str = os.path.join(dir_path, f"batch_{jj+1}.bin")
                with open(filename, "wb") as fout_b:
                    fout_b.write(batch)

        metadata = dict()
        metadata["simulations_id"] = sim_ids
        with open(os.path.join(self._cache_path, "metadata.json"), "w") as fout:
            json.dump(metadata, fout)

    def update_cache(self):
        self._logger.warning(
            f"""Update cache not yet implemented. If you need to
                             Update the cache, please use build_cache(delete_old=True"""
        )

    def _get_simulations_id(self) -> List[int]:
        with open(os.path.join(self._cache_path, "metadata.json")) as fin:
            jj = json.load(fin)
        self._simulations_id = jj["simulations_id"]

    def _get_simulations_params(self) -> List[Dict]:
        simulation_params: List[Dict] = []
        for sim_id in self.simulations_id:
            dir_path: str = os.path.join(self._cache_path, f"simulation_{sim_id}")
            with open(os.path.join(dir_path, "params.json")) as fin:
                simulation_params.append(json.load(fin))

        self._simulations_params = simulation_params

    def yield_batches(self, simulation_id: int):
        """
        Yield the batchs for a given simulation_id.
        Parameters
        ----------
        simulation_id: int
            The simulation id from which to get the batches

        Returns: yield batch
        -------

        Example usages:
        ---------------
        1.) In a for loop
        simulation_id = 5
        for batch in yield_batches(simulation_id):
            print(batch)

        2.) To get all the batches:
        all_batches = list(yield_batches(simulation_id))
        """

        dir_path: str = os.path.join(self._cache_path, f"simulation_{simulation_id}")
        ii: int = 1
        filename: str = os.path.join(dir_path, f"batch_{ii}.bin")
        while os.path.isfile(filename):
            with open(filename, "rb") as fin:
                batch_msgpack = msgpack.unpackb(snappy.uncompress(fin.read()))
            yield batch_msgpack
            ii += 1
            filename: str = os.path.join(dir_path, f"batch_{ii}.bin")

    def _prepare_trian_generator(self):

        # 0.) Get all the file-batches
        directories: List[str] = [
            os.path.join(self._cache_path, dd)
            for dd in os.listdir(self._cache_path)
            if os.path.isdir(os.path.join(self._cache_path, dd))
        ]
        files_batches: List[str] = []

        for dd in directories:
            files = [os.path.join(dd, ff) for ff in os.listdir(dd) if "batch" in ff]
            files_batches += files

        # 1.) We have to shuffle the files_batches, because we will pop files and batches
        random.shuffle(files_batches)
        assert files_batches

        test_len: int = int(max(self.TEST_RATIO * len(files_batches), 10))
        assert test_len > 10
        self._test_files = files_batches[:test_len]
        self._train_files = files_batches[test_len:]

        val_len: int = int(max(self.VALIDATION_RATIO * len(self._train_files), 10))
        assert val_len > 10
        self._validation_files = self._train_files[:val_len]
        self._train_files = files_batches[val_len:]
        random.shuffle(self._train_files)

        # Now, we are ready to yield the train data
        self._trian_generator_ready = True

    def get_data(self, files: List[str]) -> (np.ndarray, np.ndarray):
        targets: List[float] = []
        features_all: List[List[float]] = []

        for file in files:
            paramsfile: str = os.path.join(os.path.dirname(file), "params.json")
            with open(file, "rb") as fin:
                batch = msgpack.unpackb(snappy.uncompress(fin.read()))
            with open(paramsfile) as fin:
                jj = json.load(fin)
                beta: float = jj["params"]["model"]["beta"]

            for key in batch:
                taus_in = batch[key][b"taus"]
                kk = len(taus_in)
                targets.append(batch[key][b"logDeterminant"])
                taus = np.zeros(self.INPUT_SHAPE)
                auxspins = np.zeros(self.INPUT_SHAPE)
                taus[:kk] = taus_in
                auxspins[:kk] = batch[key][b"auxSpins"]
                features_curr = (taus * auxspins / beta + 3.0) / 10.0
                features_curr[kk:] = 0.0
                assert np.all(features_curr[:kk] > 0.2)
                assert np.all(features_curr[:kk] < 0.4)
                ll_t = features_curr.shape[0] - kk
                assert np.allclose(features_curr[kk:], np.zeros(ll_t))
                # np.random.shuffle(features_curr)
                features_all.append(features_curr)

        features = np.array(features_all)
        return (features, targets)

    def _get_validation_data(self):
        self._validation_data = self.get_data(self._validation_files)

    def _get_test_data(self):
        self._test_data = self.get_data(self._test_files)

    def __getitem__(self, idx: int) -> (np.ndarray, np.ndarray):

        train_files = deepcopy(self._train_files)
        INCREMENT: int = self.NUM_FILES_PER_BATCH
        train_files: List[str] = train_files[idx * INCREMENT : (idx + 1) * INCREMENT]
        # with open("idx_out.dat", "a") as fout:
        #     fout.write(f"{idx}\n")
        return self.get_data(train_files)

    # def yield_train_data(self):
    #     if not self._trian_generator_ready:
    #         self._prepare_trian_generator()
    #
    #     while True:
    #         train_files = deepcopy(self._train_files)
    #         random.shuffle(train_files)
    #         while train_files:
    #             random.shuffle(train_files)
    #             targets: List[float] = []
    #             features_all: List[List[float]] = []
    #
    #             for ii in range(self.NUM_FILES):
    #                 train_file: str = train_files.pop()
    #                 if not train_files:
    #                     break
    #                 paramsfile: str = os.path.join(
    #                     os.path.dirname(train_file), "params.json"
    #                 )
    #                 with open(train_file, "rb") as fin:
    #                     batch = msgpack.unpackb(snappy.uncompress(fin.read()))
    #                 with open(paramsfile) as fin:
    #
    #                     jj = json.load(fin)
    #                     beta: float = jj["params"]["model"]["beta"]
    #
    #                 for key in batch:
    #                     targets.append(batch[key][b"logDeterminant"])
    #                     taus = np.zeros(self.INPUT_SHAPE)
    #                     auxspins = np.zeros(self.INPUT_SHAPE)
    #                     taus_in = batch[key][b"taus"]
    #                     kk = len(taus_in)
    #                     taus[:kk] = taus_in
    #                     auxspins[:kk] = batch[key][b"auxSpins"]
    #                     features_curr = (taus * auxspins / beta + 3.0) / 10.0
    #                     features_curr[kk:] = 0.0
    #                     features_all.append(features_curr)
    #                     assert np.all(features_curr[:kk] > 0.2)
    #                     assert np.all(features_curr[:kk] < 0.4)
    #                     ll_t = features_curr.shape[0] - kk
    #                     assert np.allclose(features_curr[kk:], np.zeros(ll_t))
    #
    #             features = np.array(features_all)
    #
    #             yield (features, targets)
    #

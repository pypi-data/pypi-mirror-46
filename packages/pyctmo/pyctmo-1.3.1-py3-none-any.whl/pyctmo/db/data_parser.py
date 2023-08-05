from .postgresqldriver import PgSqlDriver
from ..utils.simplelog import SimpleLog


from typing import List, Dict
from collections import namedtuple
import shutil
import configparser
import os
import pathlib
import json
import snappy
import msgpack


class DataParser:
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

    def build_cache(self, only_dmft:bool=True, delete_old: bool = False) -> None:

        if not os.path.isdir(self._cache_path):
            os.mkdir(self._cache_path)
            os.chdir(self._cache_path)

        # 0.) get the simulations
        pgd = PgSqlDriver()
        result = None
        if only_dmft:
            result = pgd.fetchall("SELECT id FROM simulations WHERE model_name ='SIAM_Square' ")
        else:
            result = pgd.fetchall("SELECT id FROM simulations")

        sim_ids: List[int] = []
        for el in result:
            sim_ids.append(el["id"])

        for sim_id in sim_ids:
            dir_path: str = os.path.join(self._cache_path, f"simulation_{sim_id}")
            if os.path.isdir(dir_path):
                if not delete_old:
                    continue
                else:
                    raise NotImplementedError
                    # shutil.rmtree(dir_path)
                    # os.mkdir(dir_path)
            params = pgd.fetchone(
                "SELECT params FROM simulations WHERE id=%s", params=(sim_id, )
            )
            os.mkdir(dir_path)
            with open(os.path.join(dir_path, "params.json"), "w") as fout:
                json.dump(params, fout, indent=4)

            batches_rows: List[bytes] = pgd.fetchall(
                "SELECT batch from configs__batches WHERE simulation_id=%s",
                params=(sim_id,),
            )
            for (jj, batch_row) in enumerate(batches_rows):
                filename: str = os.path.join(dir_path, f"batch_{jj+1}.bin")
                with open(filename, "wb") as fout_b:
                    fout_b.write(batch_row["batch"])

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

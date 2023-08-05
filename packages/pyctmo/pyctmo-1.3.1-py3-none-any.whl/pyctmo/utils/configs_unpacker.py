# coding: utf-8
import snappy
import struct
import msgpack
import glob
import os
from typing import List


class ConfigsUnpacker:

    BATCH_NAME_PREFIX: str = "configs_"
    BATCH_NAME_SUFFIX: str = "_ctmo.bin"

    def __init__(self, folderpath:str):
        """ """
        self._cwd:str = os.getcwd()
        os.chdir(folderpath)
        self._folderpath:str = folderpath
        self._batch_files: List[str] = []

        self._batches: List[bytes] = []
        self._batches_compressed: List[bytes] = []

        self._get_batches()

        os.chdir(self._cwd)

    @property
    def batches(self)->List[bytes]:
        return self._batches

    @property
    def batches_compressed(self)->List[bytes]:
        os.chdir(self._folderpath)
        self._get_batches_compressed()
        os.chdir(self._cwd)
        return self._batches_compressed

    @property
    def batch_files(self)->List[bytes]:
        return self._batch_files


    def _get_batches(self) -> None:

        if self._batches:
            return

        batch_files = glob.glob(ConfigsUnpacker.BATCH_NAME_PREFIX + "*" + ConfigsUnpacker.BATCH_NAME_SUFFIX)
        batch_files = [ff for ff in batch_files if os.path.isfile(ff)]
        batch_files.sort()
        self._batch_files = batch_files

        for batch_file in batch_files:
            with open(batch_file, "rb") as fin:
                bb = fin.read()

            index:int = 0
            while index < len(bb):
                size = struct.unpack("<I", bb[index:index+4])[0]
                index += 4
                batch:msgpack = msgpack.unpackb(snappy.uncompress(bb[index:index+size]))
                index += size
                self._batches.append(batch)


    def _get_batches_compressed(self)->None:
        if self._batches_compressed:
            return

        self._get_batches()
        for batch in self._batches:
            self._batches_compressed.append(snappy.compress(msgpack.packb(batch)))


    


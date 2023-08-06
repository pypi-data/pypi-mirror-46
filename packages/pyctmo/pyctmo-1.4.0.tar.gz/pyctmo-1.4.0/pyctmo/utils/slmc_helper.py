import snappy
import struct
import msgpack

class SLMCHelper:

    def __init__(self):
        pass

    @staticmethod
    def save_msgpack(msgpack_data, filename:str):
        with open(filename, "wb") as fout:
            msgpack_compressed = snappy.compress(msgpack.packb(msgpack_data))
            output_bin = struct.pack("<I", len(msgpack_compressed))
            output_bin += msgpack_compressed
            fout.write(output_bin)

    @staticmethod
    def read_msgpack(filename:str):
        with open(filename, "rb") as fin:
            data_bin = fin.read()

        index:int = 0
        len_msg = struct.unpack("<I", data_bin[index:index+4])[0]
        index += 4
        msgpack_data:msgpack = msgpack.unpackb(snappy.uncompress(data_bin[index:index+len_msg]))
        return msgpack_data


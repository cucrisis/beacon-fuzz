import importlib
import struct

from eth2spec.config import config_util
from eth2spec.phase0 import spec

CONFIGS_PATH = "/eth2/eth2.0-specs/configs"


def FuzzerInit(bls_disabled: bool) -> None:
    config_util.prepare_config(CONFIGS_PATH, "mainnet")
    importlib.reload(spec)
    # do nothing
    pass


def FuzzerRunOne(fuzzer_input):
    if len(fuzzer_input) < 2 + 32:
        return None
    count = spec.bytes_to_int(fuzzer_input[:2]) % 100
    seed = fuzzer_input[2:34]
    res = [
        spec.compute_shuffled_index(index=i, index_count=count, seed=seed)
        for i in range(count)
    ]
    ret = bytes()
    for r in res:
        ret += struct.pack("<Q", r)
    return ret

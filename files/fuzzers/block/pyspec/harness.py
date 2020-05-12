import importlib
import typing

from eth2spec.config import config_util
from eth2spec.phase0 import spec
from eth2spec.utils import bls
from eth2spec.utils.ssz.ssz_impl import serialize

# TODO fix up so not hard-coded
CONFIGS_PATH = "/eth2/eth2.0-specs/configs"


VALIDATE_STATE_ROOT = True


BlockTestCase = None


def FuzzerInit(bls_disabled: bool) -> None:
    global BlockTestCase
    config_util.prepare_config(CONFIGS_PATH, "mainnet")
    importlib.reload(spec)

    if bls_disabled:
        bls.bls_active = False

    # NOTE: we need to define the test case after reloading the spec
    class BlockTestCaseImpl(spec.Container):
        pre: spec.BeaconState
        block: spec.SignedBeaconBlock

    BlockTestCase = BlockTestCaseImpl


def FuzzerRunOne(input_data: bytes) -> typing.Optional[bytes]:
    state_block = BlockTestCase.decode_bytes(input_data)

    try:
        poststate = spec.state_transition(
            state=state_block.pre,
            signed_block=state_block.block,
            validate_result=VALIDATE_STATE_ROOT,
        )
    except (AssertionError, IndexError):
        return None

    return serialize(poststate)

import importlib
import typing

from eth2spec.config import config_util
from eth2spec.phase0 import spec
from eth2spec.utils import bls
from eth2spec.utils.ssz.ssz_impl import serialize

# TODO(gnattishness) fix config path difficult to do unless we assume the eth2spec
# module is at a fixed position relative to the configs
# (i.e. it is inside a cloned eth2.0-specs repo)
CONFIGS_PATH = "/eth2/eth2.0-specs/configs"

ProposerSlashingTestCase = None


def FuzzerInit(bls_disabled: bool) -> None:
    global ProposerSlashingTestCase
    config_util.prepare_config(CONFIGS_PATH, "mainnet")
    importlib.reload(spec)

    if bls_disabled:
        bls.bls_active = False

    class ProposerSlashingTestCaseImpl(spec.Container):
        pre: spec.BeaconState
        proposer_slashing: spec.ProposerSlashing

    ProposerSlashingTestCase = ProposerSlashingTestCaseImpl


def FuzzerRunOne(input_data: bytes) -> typing.Optional[bytes]:
    test_case = ProposerSlashingTestCase.decode_bytes(input_data)

    try:
        # modifies state in place
        spec.process_proposer_slashing(test_case.pre, test_case.proposer_slashing)
    except (AssertionError, IndexError):
        return None

    return serialize(test_case.pre)

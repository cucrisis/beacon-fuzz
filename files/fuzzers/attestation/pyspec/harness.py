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

AttestationTestCase = None


def FuzzerInit(bls_disabled: bool) -> None:
    global AttestationTestCase
    config_util.prepare_config(CONFIGS_PATH, "mainnet")
    importlib.reload(spec)

    if bls_disabled:
        bls.bls_active = False

    # NOTE: we need to define the test case after reloading the spec
    class AttestationTestCaseImpl(spec.Container):
        pre: spec.BeaconState
        attestation: spec.Attestation

    AttestationTestCase = AttestationTestCaseImpl


def FuzzerRunOne(input_data: bytes) -> typing.Optional[bytes]:
    test_case = AttestationTestCase.decode_bytes(input_data)

    try:
        # modifies state in place
        spec.process_attestation(test_case.pre, test_case.attestation)
        # NOTE - signature verification should do nothing with bls disabled
    except (AssertionError, IndexError):
        return None

    return serialize(test_case.pre)

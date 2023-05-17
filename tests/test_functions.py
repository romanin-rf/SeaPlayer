import os
import pytest
from seaplayer.functions import is_midi_file

# ! Vars
LOCAL_DIRPATH = os.path.dirname(__file__)

# ! Getting
def get_clibration_filepath(filename: str) -> str:
    return os.path.join(LOCAL_DIRPATH, "calibration_data", filename)

# ! Tests
def test_is_midi_file():
    assert is_midi_file(get_clibration_filepath("test.mid"))


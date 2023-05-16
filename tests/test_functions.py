import os
import pytest
try:
    from seaplayer.functions import is_midi_file
    IMPORTED = True
except:
    IMPORTED = False

# ! Vars
LOCAL_DIRPATH = os.path.dirname(__file__)

# ! Getting
def get_clibration_filepath(filename: str) -> str:
    return os.path.join(LOCAL_DIRPATH, "calibration_data", filename)

# ! Tests
if IMPORTED:
    def test_is_midi_file():
        assert is_midi_file(get_clibration_filepath("test.mid"))


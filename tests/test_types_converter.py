import os
import pytest
from seaplayer.types import Converter
from seaplayer.exceptions import PathNotExistsError

# ! Vars
LOCAL_DIRPATH = os.path.dirname(__file__)
conv = Converter()

# ! Getting
def get_clibration_filepath(filename: str) -> str:
    return os.path.join(LOCAL_DIRPATH, "calibration_data", filename)

# ! Tests
def test_optional():
    assert conv.optional(conv.boolean)("True")
    assert conv.optional(str)("None") is None

def test_literal_string():
    l = conv.literal_string("name", "value", "test")
    assert l("name") == "name"
    with pytest.raises(RuntimeError, match="is not in the list of values."):
        l("haha")

def test_union():
    decimal = conv.union(float, int)
    assert decimal("12.0") == 12.0
    assert decimal("11") == 11
    
    conv_types = conv.union( conv.boolean, conv.optional(conv.literal_string("unknown", "dead")) )
    assert conv_types("True")
    assert conv_types("None") is None
    assert conv_types("unknown") is not None
    with pytest.raises(TypeError):
        conv_types("...")

def test_path():
    exist_path = get_clibration_filepath("test.mid")
    not_exist_path = get_clibration_filepath("not_exist.mp3")
    exist_dirpath = get_clibration_filepath("")
    
    assert conv.path(exist_path) == exist_path
    assert conv.path(exist_dirpath) == exist_dirpath
    with pytest.raises(PathNotExistsError):
        conv.path(not_exist_path)

def test_filepath():
    exist_path = get_clibration_filepath("test.mid")
    not_exist_path = get_clibration_filepath("not_exist.mp3")
    exist_dirpath = get_clibration_filepath("")
    
    assert conv.filepath(exist_path) == exist_path
    with pytest.raises(PathNotExistsError):
        conv.filepath(not_exist_path)
        conv.filepath(exist_dirpath)


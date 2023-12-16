import os
import pytest
from seaplayer.languages import LanguageLoader
from seaplayer.units import LANGUAGES_DIRPATH

# ! Vars
ll = LanguageLoader(LANGUAGES_DIRPATH, "en-eng")

# ! Tests
def test_language_count_loaded():
    assert len(ll.langs) >= len(os.listdir(LANGUAGES_DIRPATH))

def test_language_get_not_exist():
    assert ll.get("") == "<LTNF>"

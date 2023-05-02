import os
import platform
from typing import Dict, List

if platform.system() == "Windows": ds = ";"
elif platform.system() == "Linux": ds = ":"
else: raise RuntimeError("Your operating system is not supported.")

LOCALDIR = os.getcwd()
TRASH_FILES = [
    "build", "SeaPlayer.spec"
]
DATA = {
    # * 1) Main Files
    "seaplayer": "seaplayer/",
    "seaplayer/__init__.py": "seaplayer/",
    "seaplayer/__main__.py": "seaplayer/",
    "seaplayer/functions.py": "seaplayer/",
    "seaplayer/objects.py": "seaplayer/",
    "seaplayer/seaplayer.py": "seaplayer/",
    "seaplayer/types.py": "seaplayer/",
    "seaplayer/config.py": "seaplayer/",
    "seaplayer/screens.py": "seaplayer/",
    # * 2) Modules Files
    "seaplayer/modules": "seaplayer/modules/",
    "seaplayer/modules/__init__.py": "seaplayer/modules/",
    # * 2.1) AsyncTPNG
    "seaplayer/modules/asynctpng": "seaplayer/modules/asynctpng/",
    "seaplayer/modules/asynctpng/__init__.py": "seaplayer/modules/asynctpng/",
    "seaplayer/modules/asynctpng/tpng.py": "seaplayer/modules/asynctpng/",
    "seaplayer/modules/asynctpng/tpng.pyi": "seaplayer/modules/asynctpng/",
    # * 3) CSS Files
    "seaplayer/css": "seaplayer/css/",
    "seaplayer/css/seaplayer.css": "seaplayer/css/",
    "seaplayer/css/configurate.css": "seaplayer/css/",
    "seaplayer/css/unknown.css": "seaplayer/css/"
}

def localize(path: str) -> str: return os.path.join(LOCALDIR, path.replace('/', os.sep).replace('\\', os.sep))
def add_datas(data: Dict[str, str]) -> List[str]: return [f"--add-data \"{localize(path)}{ds}{data[path]}\"" for path in data]

COMMAND_LINE = [
    "pyinstaller", "--noconfirm", "--console", "--clean", "--onefile",
    f"--icon \"{localize('icons/sea_player-icon-200x200.ico')}\"",
    *add_datas(DATA),
    f"\"{localize('SeaPlayer.py')}\""
]
COMMAND = " ".join(COMMAND_LINE)

print(COMMAND, end="\n\n")
os.system(COMMAND)

for path in TRASH_FILES:
    try: os.remove(localize(path))
    except: pass
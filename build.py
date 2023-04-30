import os
import platform
from typing import Dict, List

if platform.system() == "Windows": ds = ";"
elif platform.system() == "Linux": ds = ":"
else: raise RuntimeError("Your operating system is not supported.")

LOCALDIR = os.getcwd()
DATA = {
    "seaplayer/ui.css": "seaplayer/",
    "seaplayer": "seaplayer/",
    "seaplayer/__init__.py": "seaplayer/",
    "seaplayer/__main__.py": "seaplayer/",
    "seaplayer/functions.py": "seaplayer/",
    "seaplayer/objects.py": "seaplayer/",
    "seaplayer/seaplayer.py": "seaplayer/",
    "seaplayer/types.py": "seaplayer/",
    "seaplayer/asynctpng": "seaplayer/asynctpng/",
    "seaplayer/asynctpng/__init__.py": "seaplayer/asynctpng/",
    "seaplayer/asynctpng/tpng.py": "seaplayer/asynctpng/",
    "seaplayer/asynctpng/tpng.pyi": "seaplayer/asynctpng/"
}

def localize(path: str) -> str: return os.path.join(LOCALDIR, path.replace('/', os.sep).replace('\\', os.sep))
def add_datas(data: Dict[str, str]) -> List[str]: return [f"--add-data \"{localize(path)}{ds}{data[path]}\"" for path in data]

COMMAND = [
    "pyinstaller", "--noconfirm", "--onefile", "--console", "--clean",
    f"--icon \"{localize('icons/sea_player-icon-200x200.ico')}\"",
    *add_datas(DATA),
    f"\"{localize('SeaPlayer.py')}\""
]

os.system(" ".join(COMMAND))
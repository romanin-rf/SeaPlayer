import os
import shutil
import platform
from pathlib import Path
from typing import Dict, List

if platform.system() == "Windows": ds = ";"
elif platform.system() == "Linux": ds = ":"
else: raise RuntimeError("Your operating system is not supported.")

LOCALDIR = os.getcwd()
TRASH_FILES = [ "build", "SeaPlayer.spec" ]
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
    "seaplayer/exceptions.py": "seaplayer/",
    "seaplayer/codeсbase.py": "seaplayer/",
    "seaplayer/codecs.py": "seaplayer/",
    # * 2) Modules Files
    "seaplayer/modules": "seaplayer/modules/",
    "seaplayer/modules/__init__.py": "seaplayer/modules/",
    "seaplayer/modules/colorizer.py": "seaplayer/modules/",
    # * 3) CSS Files
    "seaplayer/css": "seaplayer/css/",
    "seaplayer/css/seaplayer.css": "seaplayer/css/",
    "seaplayer/css/configurate.css": "seaplayer/css/",
    "seaplayer/css/unknown.css": "seaplayer/css/",
    # * 4) Assets Files
    "seaplayer/assets": "seaplayer/assets/",
    "seaplayer/assets/image-not-found.png": "seaplayer/assets/"
}

def localize(path: str) -> str: return os.path.join(LOCALDIR, path.replace('/', os.sep).replace('\\', os.sep))
def add_datas(data: Dict[str, str]) -> List[str]: return [f"--add-data \"{localize(path)}{ds}{data[path]}\"" for path in data]

COMMAND_LINE = [
    "pyinstaller", "--noconfirm", "--console", "--clean", "--onefile",
    f"--icon \"{localize('icons/icon.ico')}\"",
    *add_datas(DATA),
    f"\"{localize('SeaPlayer.py')}\""
]
COMMAND = " ".join(COMMAND_LINE)

print(COMMAND, end="\n\n")
os.system(COMMAND)

for i in TRASH_FILES:
    path = Path(localize(i))
    try:
        if path.is_dir():
            shutil.rmtree(path.name, ignore_errors=True)
        else:
            os.remove(path.name)
    except:
        pass
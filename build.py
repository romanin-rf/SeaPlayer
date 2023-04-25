import os
import platform

if platform.system() == "Windows": ds = ";"
elif platform.system() == "Linux": ds = ":"
else: raise RuntimeError("Your operating system is not supported.")

LOCALDIR = os.getcwd()

COMMAND = [
    "pyinstaller", "--noconfirm", "--onefile", "--console", "--clean",
    f"--icon \"{os.path.join(LOCALDIR, 'icons', 'sea_player-icon-200x200.ico')}\"",
    f"--add-data \"{os.path.join(LOCALDIR, 'ui.css')}{ds}.\"",
    f"\"{os.path.join(LOCALDIR, 'sea_player.py')}\""
]
os.system(" ".join(COMMAND))
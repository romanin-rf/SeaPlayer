@echo off
set localdir=%сd%
pyinstaller --noconfirm --onefile --console --icon "%localdir%\icons\sea_player-icon-200x200.ico" --clean --add-data "%localdir%\ui.css;." "%localdir%\sea_player.py"

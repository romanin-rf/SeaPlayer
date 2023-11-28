import sys
import subprocess
from typing import Tuple

# ! Main Class
class PIPManager:
    def __init__(self) -> None:
        self.python_path = sys.executable
    
    def __call__(self, *args: str) -> Tuple[int, str]:
        return subprocess.getstatusoutput(" ".join([self.python_path, "-m", *args]))
    
    def install(self, *args: str) -> bool:
        code, output = self.__call__("install", *args)
        return code == 0

# ! Initial
pip = PIPManager()
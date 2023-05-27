import os
import pickle
# > Typing
from typing import TypeVar, Any

# ! T
D = TypeVar("D")

# ! Main Class
class Cacher:
    def __init__(self, cache_dirpath: str) -> None:
        self.main_dirpath = os.path.abspath(cache_dirpath)
        self.vars_dirpath = os.path.join(self.main_dirpath, "vars")

        # * Create Directory
        os.makedirs(self.main_dirpath, 0o755, True)
        os.makedirs(self.vars_dirpath, 0o755, True)

        # * Check Directory
        assert os.path.isdir(self.main_dirpath)
        assert os.path.isdir(self.vars_dirpath)
    
    def write(self, data: Any, filepath: str) -> None:
        with open(filepath, "wb") as file:
            pickle.dump(data, file)
    
    def read(self, filepath: str, default: D) -> D:
        try:
            with open(filepath, "rb") as file:
                return pickle.load(file)
        except:
            self.write(default, filepath)
            return default
    
    def write_var(self, value: Any, name: str, *, group: str="main") -> None: self.write(value, os.path.join(self.vars_dirpath, f"{name}-{group}.pycache"))
    def read_var(self, name: str, default: D, *, group: str="main") -> D: return self.read(os.path.join(self.vars_dirpath, f"{name}-{group}.pycache"), default)
    
    def var(self, name: str, default: D, *, group: str="main") -> D:
        def setter(s, value: D) -> None: self.write_var(value, name, group=group)
        def getter(s) -> D: return self.read_var(name, default, group=group)
        return property(getter, setter)

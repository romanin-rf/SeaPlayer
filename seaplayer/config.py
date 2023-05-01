import properties
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_CONFIG_DATA = {
    "sound_font_path": None,
    "volume_change_percent": 0.01,
    "rewind_count_seconds": 1,
    "recursive_search": False
}

class SeaPlayerConfig:
    @staticmethod
    def dump(filepath: Path, data: Dict[str, Any]) -> None:
        with open(filepath, "w", encoding="utf-8", errors="ignore") as file:
            properties.dump(data, file)
    
    @staticmethod
    def load(filepath: Path, default: Dict[str, Any]) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            try: return properties.load(file)
            except: pass
        with open(filepath, "w", encoding="utf-8", errors="ignore") as file:
            properties.dump(default, file)
        return default
    
    def refresh(self) -> None: self.dump(self.filepath, self.config)
    
    def __init__(
        self,
        filepath: str,
        *,
        default_data: Dict[str, Any]=DEFAULT_CONFIG_DATA
    ) -> None:
        self.filepath = Path(filepath)
        self.default_data = default_data
        if self.filepath.exists():
            self.config = self.load(self.filepath, self.default_data)
        else:
            self.config = default_data
            self.refresh()
    
    def get(self, key: str) -> Any: return self.config.get(key)
    def set(self, key: str, value: Any): self.config[key] = value ; self.refresh()
    
    
    @property
    def sound_font_path(self) -> Optional[str]: return self.get("sound_font_path")
    @sound_font_path.setter
    def sound_font_path(self, value: Any): self.set("sound_font_path", value)
    
    @property
    def volume_change_percent(self) -> float: return self.get("volume_change_percent")
    @volume_change_percent.setter
    def volume_change_percent(self, value: Any): self.set("volume_change_percent", value)
    
    @property
    def rewind_count_seconds(self) -> int: return self.get("rewind_count_seconds")
    @rewind_count_seconds.setter
    def rewind_count_seconds(self, value: Any): self.set("rewind_count_seconds", value)
    
    @property
    def recursive_search(self) -> bool: return self.get("recursive_search")
    @recursive_search.setter
    def recursive_search(self, value: Any): self.set("recursive_search", value)
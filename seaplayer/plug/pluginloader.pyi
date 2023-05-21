from pathlib import Path
from pydantic import BaseModel
# > Typing
from typing import Optional, Dict, Union, Any, AsyncGenerator, Tuple

# ! Plugin Loader Config
class PluginLoaderConfigModel(BaseModel):
    plugins_enable: Dict[str, bool] = {}

class PluginLoaderConfigManager:
    filepath: Path
    config: PluginLoaderConfigModel
    
    @staticmethod
    def dump(path: str, data: PluginLoaderConfigModel) -> None: ...
    @staticmethod
    def load(path: str, default_data: Dict[str, Any]) -> PluginLoaderConfigModel: ...
    
    def refresh(self) -> None: ...
    def __init__(self, path: str) -> None: ...

# ! Plugin Loader Class
class PluginLoader:
    def __init__(
        self,
        plugins_dirpath: Optional[Union[str, Path]]=None,
        plugins_config_path: Optional[Union[str, Path]]=None,
        *args,
        **kwargs
    ) -> None:
        ...
    
    async def search_plugins_paths(self) -> AsyncGenerator[Tuple[str, str]]: ...
    
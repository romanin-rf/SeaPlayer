from pathlib import Path
from pydantic import BaseModel
# > Typing
from types import ModuleType
from typing import (
    Any,
    Dict,
    List,
    Type,
    Tuple,
    Union,
    Optional,
    Generator, 
    AsyncGenerator
)
# > Local Import's
from .pluginbase import PluginBase, PluginInfo
from ..seaplayer import SeaPlayer

# ! Types
class PluginModuleType(ModuleType):
    plugin_main: Type[PluginBase]

# ! Functions
def get_module_info(path: str) -> Tuple[str, str]: ...
def load_module(path: str) -> PluginModuleType: ...
def plugin_from_module(app: SeaPlayer, pl: PluginLoader, info: PluginInfo, module: PluginModuleType) -> PluginBase: ...

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

    def exists_plugin(self, info: PluginInfo) -> bool: ...
    def add_plugin(self, info: PluginInfo) -> None: ...
    def is_enable_plugin(self, info: PluginInfo) -> bool: ...

# ! Plugin Loader Class
class PluginLoader:
    app: SeaPlayer
    plugins_dirpath: Path
    plugins_config_path: Path
    on_plugins: List[PluginBase]
    off_plugins: List[PluginInfo]
    error_plugins: List[Tuple[str, str]]

    def __init__(
        self,
        app: SeaPlayer,
        plugins_dirpath: Optional[Union[str, Path]]=None,
        plugins_config_path: Optional[Union[str, Path]]=None,
        *args,
        **kwargs
    ) -> None:
        ...
    
    async def aio_search_plugins_paths(self) -> AsyncGenerator[Tuple[str, str]]: ...
    def search_plugins_paths(self) -> Generator[Tuple[str, str], Any, None]: ...

    def on_init(self) -> None: ...
    def on_run(self) -> None: ...
    async def on_compose(self) -> None: ...
    async def on_quit(self) -> None: ...
    
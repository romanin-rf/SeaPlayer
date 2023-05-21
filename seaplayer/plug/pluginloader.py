import os
import glob
import asyncio
from pathlib import Path
from pydantic import BaseModel
# > Typing
from typing import Optional, Dict, Union, AsyncGenerator, Tuple, Any
# > Local Import's
from ..functions import aiter
from ..units import (
    PLUGINS_DIRPATH,
    PLUGINS_CONFIG_PATH,
    GLOB_PLUGINS_INFO_SEARCH,
    GLOB_PLUGINS_INIT_SEARCH
)

# ! Plugin Loader Config
class PluginLoaderConfigModel(BaseModel):
    plugins_enable: Dict[str, bool]

class PluginLoaderConfigManager:
    @staticmethod
    def dump(data: PluginLoaderConfigModel, path: str) -> None:
        with open(path, 'w') as file:
            file.write(data.json())
    
    @staticmethod
    def load(path: str) -> PluginLoaderConfigModel:
        return PluginLoaderConfigModel.parse_file(path)
    
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        

# ! Plugin Loader Class
class PluginLoader:
    def __init__(
        self,
        plugins_dirpath: Optional[Union[str, Path]]=None,
        plugins_config_path: Optional[Union[str, Path]]=None,
        *args,
        **kwargs
    ) -> None:
        self.plugins_dirpath = Path(os.path.abspath(plugins_dirpath or PLUGINS_DIRPATH))
        self.plugins_config_path = Path(os.path.abspath(plugins_config_path or PLUGINS_CONFIG_PATH))
        
        # * Create plugins directory
        os.makedirs(self.plugins_dirpath, 0o755, True)
        
        # * Config Initializing
        self.config = PluginLoaderConfigManager(self.plugins_config_path)
        
        # * Vars
        self.plugins = []
        self.on_plugins = []
        self.off_plugins = []
    
    async def search_plugins_paths(self): # -> AsyncGenerator[Tuple[str, str]]
        info_search, init_search = glob.glob(GLOB_PLUGINS_INFO_SEARCH), glob.glob(GLOB_PLUGINS_INIT_SEARCH)
        async for info_path in aiter(info_search):
            info_dirpath = os.path.dirname(info_path)
            async for init_path in aiter(init_search):
                init_dirpath = os.path.dirname(init_path)
                if init_dirpath == info_dirpath:
                    yield info_path, init_path
                    await asyncio.sleep(0)
    
    
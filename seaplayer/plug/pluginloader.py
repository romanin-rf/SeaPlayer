import os
import sys
import glob
import asyncio
from pathlib import Path
from pydantic import BaseModel
# > ImportLib
from importlib.util import spec_from_file_location, module_from_spec
# > Typing
from types import ModuleType
from typing import Optional, Dict, Union, Any, List, Tuple, Type
# > Local Import's
from .pluginbase import PluginInfo, PluginBase
from ..functions import aiter
from ..units import (
    PLUGINS_DIRPATH,
    PLUGINS_CONFIG_PATH,
    GLOB_PLUGINS_INFO_SEARCH,
    GLOB_PLUGINS_INIT_SEARCH
)

# ! Types
class PluginModuleType(ModuleType):
    plugin_main: Type[PluginBase]

# ! Functions
def get_module_info(path: str):
    if os.path.basename(path) == "__init__.py":
        return os.path.basename(os.path.dirname(path)), path
    return os.path.basename(path), path

def get_submodules_locations(init_path: str) -> List[str]:
    return [ os.path.dirname(init_path) ]

def load_module(init_path: str) -> PluginModuleType:
    module_name, module_location = get_module_info(init_path)
    module_spec = spec_from_file_location(
        module_name,
        module_location,
        submodule_search_locations=get_submodules_locations(init_path)
    )
    module = module_from_spec(module_spec)
    
    sys.modules[module_spec.name] = module 
    # TODO: Temporary option as there is a risk of replacing existing modules
    # TODO: Make an environment-module to surround all these modules for security
    
    module_spec.loader.exec_module(module)
    return module

def plugin_from_module(app, pl, info: PluginInfo, module: PluginModuleType) -> PluginBase:
    return module.plugin_main(app, pl, info)

# ! Plugin Loader Config
class PluginLoaderConfigModel(BaseModel):
    plugins_enable: Dict[str, bool] = {}

class PluginLoaderConfigManager:
    @staticmethod
    def dump(path: str, data: PluginLoaderConfigModel) -> None:
        with open(path, 'w') as file:
            file.write(data.json())
    
    @staticmethod
    def load(path: str, default_data: Dict[str, Any]) -> PluginLoaderConfigModel:
        try:
            return PluginLoaderConfigModel.parse_file(path)
        except:
            return default_data
    
    def refresh(self) -> None: self.dump(self.filepath, self.config)
    
    def __init__(self, path: str) -> None:
        self.filepath = Path(path)
        
        default_data  = PluginLoaderConfigModel().dict()
        if self.filepath.exists():
            self.config = self.load(self.filepath, default_data)
            config_temp = default_data.copy()
            config_temp.update(self.config)
            self.config = PluginLoaderConfigModel.parse_obj(config_temp)
        else:
            self.config = PluginLoaderConfigModel.parse_obj(default_data)
        self.refresh()
    
    def exists_plugin(self, info: PluginInfo) -> bool:
        return info.name_id in self.config.plugins_enable.keys()
    
    def exists_plugin_by_name_id(self, name_id: str) -> bool:
        return name_id in self.config.plugins_enable.keys()
    
    def add_plugin(self, info: PluginInfo) -> None:
        self.config.plugins_enable[info.name_id] = True
        self.refresh()
    
    def is_enable_plugin(self, info: PluginInfo) -> bool:
        for name_id, enable in self.config.plugins_enable.items():
            if name_id == info.name_id:
                return enable
        return False
    
    def disable_plugin(self, info: PluginInfo) -> None:
        self.config.plugins_enable[info.name_id] = False
        self.refresh()
    
    def disable_plugin_by_name_id(self, name_id: str) -> None:
        self.config.plugins_enable[name_id] = False
        self.refresh()
    
    def enable_plugin(self, info: PluginInfo) -> None:
        self.config.plugins_enable[info.name_id] = True
        self.refresh()
    
    def enable_plugin_by_name_id(self, name_id: str) -> None:
        self.config.plugins_enable[name_id] = True
        self.refresh()

# ! Plugin Loader Class
class PluginLoader:
    __title__: str = "PluginLoader"
    __version__: str = "0.1.3"
    __author__: str = "Romanin"
    __email__: str = "semina054@gmail.com"

    def __init__(
        self,
        app,
        plugins_dirpath: Optional[Union[str, Path]]=None,
        plugins_config_path: Optional[Union[str, Path]]=None,
        *args,
        **kwargs
    ) -> None:
        self.app = app
        self.plugins_dirpath = Path(os.path.abspath(plugins_dirpath or PLUGINS_DIRPATH))
        self.plugins_config_path = Path(os.path.abspath(plugins_config_path or PLUGINS_CONFIG_PATH))
        
        # * Create plugins directory
        os.makedirs(self.plugins_dirpath, 0o755, True)
        
        # * Config Initializing
        self.config = PluginLoaderConfigManager(self.plugins_config_path)
        
        # * Vars
        self.on_plugins: List[PluginBase] = []
        self.off_plugins: List[PluginInfo] = []
        self.error_plugins: List[Tuple[str, str]] = []
        
        # * Logging
        self.app.info("---")
    
    @staticmethod
    async def aio_search_plugins_paths():
        info_search, init_search = glob.glob(GLOB_PLUGINS_INFO_SEARCH), glob.glob(GLOB_PLUGINS_INIT_SEARCH)
        async for info_path in aiter(info_search):
            info_dirpath = os.path.dirname(info_path)
            async for init_path in aiter(init_search):
                init_dirpath = os.path.dirname(init_path)
                if init_dirpath == info_dirpath:
                    yield info_path, init_path
                    await asyncio.sleep(0)
    
    @staticmethod
    def search_plugins_paths():
        info_search, init_search = glob.glob(GLOB_PLUGINS_INFO_SEARCH), glob.glob(GLOB_PLUGINS_INIT_SEARCH)
        for info_path in info_search:
            info_dirpath = os.path.dirname(info_path)
            for init_path in init_search:
                init_dirpath = os.path.dirname(init_path)
                if init_dirpath == info_dirpath:
                    yield info_path, init_path
    
    @staticmethod
    def load_plugin_info(path: str) -> PluginInfo: return PluginInfo.parse_file(path)
    
    def on_init(self) -> None:
        self.app.info(f"{self.__title__} v{self.__version__} from {self.__author__} ({self.__email__})")
        plugins_paths = list(self.search_plugins_paths())
        self.app.info(f"Found plugins        : {repr([os.path.basename(os.path.dirname(i[0])) for i in plugins_paths])}")
        for info_path, init_path in plugins_paths:
            info = None
            try:
                info = self.load_plugin_info(info_path)

                if not self.config.exists_plugin(info):
                    self.config.add_plugin(info)
                
                if self.config.is_enable_plugin(info):
                    plugin_module = load_module(init_path)
                    plugin = plugin_from_module(self.app, self, info, plugin_module)

                    try:
                        plugin.on_init()
                    except:
                        self.app.info(f"Failed to do [green]`on_init`[/green] in: {plugin}")
                    
                    self.on_plugins.append(plugin)
                else:
                    self.off_plugins.append(info)
            except Exception as e:
                self.error_plugins.append( (info_path, init_path) )
                if info is not None:
                    self.app.info(f"Failed to load plugin: {repr(info)}")
                else:
                    self.app.info(f"Failed to load plugin: {repr(os.path.basename(os.path.dirname(info_path)))}")
                raise e
        self.app.info(f"Plugins loaded ([green]ON [/green]) : {repr(self.on_plugins)}")
        self.app.info(f"Plugins loaded ([red]OFF[/red]) : {repr(self.off_plugins)}")
    
    def on_run(self) -> None:
        for i in self.on_plugins:
            try:
                i.on_run()
            except:
                self.app.info(f"Failed to do [green]`on_run`[/green] in: {i}")

    async def on_compose(self) -> None:
        async for i in aiter(self.on_plugins):
            try:
                await i.on_compose()
            except:
                self.app.info(f"Failed to do [green]`await on_compose`[/green] in: {i}")
    
    async def on_quit(self) -> None:
        async for i in aiter(self.on_plugins):
            try:
                await i.on_quit()
            except:
                self.app.info(f"Failed to do [green]`await on_quit`[/green] in: {i}")

import os
from rich.console import Console
# > Typing
from typing import List
# > Local Import's
from .functions import *
from ..pluginbase import PluginInfo
from ..pluginloader import PluginLoaderConfigManager, PluginLoader, load_plugin_info
from ...units import PLUGINS_CONFIG_PATH, PLUGINS_DIRPATH

# ! Vars
console = Console()

# ! Functions
def init_config() -> None:
    os.makedirs(PLUGINS_DIRPATH, mode=0o755, exist_ok=True)
    os.makedirs(os.path.dirname(PLUGINS_CONFIG_PATH), mode=0o755, exist_ok=True)
    plugin_config, plugins_infos = PluginLoaderConfigManager(PLUGINS_CONFIG_PATH), get_plugins_info()
    add_plugins(plugin_config, *plugins_infos)

def is_config_inited() -> bool:
    try:
        assert os.path.exists(PLUGINS_DIRPATH)
        assert os.path.exists(os.path.dirname(PLUGINS_CONFIG_PATH))
        assert os.path.exists(PLUGINS_CONFIG_PATH)
    except:
        return False
    return True

def add_plugins(
    plugin_config: PluginLoaderConfigManager,
    *infos: PluginInfo
) -> None:
    for info in infos:
        if not plugin_config.exists_plugin(info):
            plugin_config.add_plugin(info)

def get_plugins_info() -> List[PluginInfo]:
    plugins_infos = []
    for plugin_init_path, plugin_info_path, plugin_deps_path in PluginLoader.search_plugins_paths():
        try:
            plugins_infos.append(load_plugin_info(plugin_info_path))
        except:
            console.print_exception()
    return plugins_infos

def is_plugin_dirpath(dirpath: str) -> bool:
    try:
        assert os.path.exists(dirpath)
        assert os.path.exists(os.path.join(dirpath, "info.json"))
        assert os.path.exists(os.path.join(dirpath, "__init__.py"))
        PluginInfo.model_validate_json(open(os.path.join(dirpath, "info.json"), "rb").read())
    except:
        return False
    return True

# ! Other
def raise_exception(console: Console, exc_type: Exception, *args, **kwargs) -> None:
    try: raise exc_type(*args, **kwargs)
    except: console.print_exception()
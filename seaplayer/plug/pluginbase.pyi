from pydantic import BaseModel
from textual.screen import Screen
from textual.binding import Binding
# > Typing
from typing import Optional, Generator, Type, Callable, List, Any
# > Local Import's
from ..seaplayer import SeaPlayer
from ..codeсbase import CodecBase
from .pluginloader import PluginLoader

# ! Plugin Info Class
class PluginInfo(BaseModel):
    name: str
    name_id: str
    version: str
    author: str
    description: Optional[str]=None
    url: Optional[str]=None

# ! Plugin Base Class
class PluginBase:
    app: SeaPlayer
    pl: PluginLoader
    info: PluginInfo
    
    def __init_repr__(self) -> str: ...
    def __init__(self, app: SeaPlayer, pl: PluginLoader, info: PluginInfo) -> None: ...
    # ! App Specific Methods
    def install_screen(self, name: str, screen: Screen) -> None: ...
    def add_codecs(self, *codecs: Type[CodecBase]) -> None: ...
    def add_value_handlers(self, *handlers: Callable[[str], List[str]]) -> None: ...
    def on_bindings(self) -> Generator[Binding, Any, None]: ...
    # ! App On Methods
    def on_init(self) -> None: ...
    def on_run(self) -> None: ...
    async def on_compose(self) -> None: ...
    async def on_ready(self) -> None: ...
    async def on_quit(self) -> None: ...

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
    """The base class of the plugin."""
    app: SeaPlayer
    """A link to the image of the `SeaPlayer` class."""
    pl: PluginLoader
    """A link to the image of the `PluginLoader` class."""
    info: PluginInfo
    """Contains all variables from `info.json`."""
    
    def __init_repr__(self) -> str:
        """The string that is output to the logs after initialization of the class.
        
        Returns:
            str: A string indicating the initialization of the class.
        """
        ...
    def __init__(self, app: SeaPlayer, pl: PluginLoader, info: PluginInfo) -> None:
        """The base class of the plugin.
        
        Args:
            app (SeaPlayer): A link to the image of the `SeaPlayer` class.
            pl (PluginLoader): A link to the image of the `PluginLoader` class.
            info (PluginInfo): Contains all variables from `info.json`.
        """
        ...
    # ! App Specific Methods
    def install_screen(self, name: str, screen: Screen) -> None:
        """Adding a new `Screen`.
        
        Args:
            name (str): The name by which it will be accessed by SeaPlayer.
            screen (Screen): The image of the `Screen` class.
        """
        ...
    def add_codecs(self, *codecs: Type[CodecBase]) -> None:
        """Adding codecs."""
        ...
    def add_value_handlers(self, *handlers: Callable[[str], List[str]]) -> None:
        """Adding handlers for user-entered values."""
        ...
    # ! App Specific On Methods
    def on_bindings(self) -> Generator[Binding, Any, None]:
        """A generator for binding information classes about keys.
        
        Yields:
            Generator[Binding, Any, None]: A class with information about key bindings.
        """
        ...
    # ! App On Methods
    def on_init(self) -> None: ...
    def on_run(self) -> None: ...
    async def on_compose(self) -> None: ...
    async def on_ready(self) -> None: ...
    async def on_quit(self) -> None: ...

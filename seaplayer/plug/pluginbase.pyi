from pydantic import BaseModel
# > Typing
from typing import Optional
# > Local Import's
from ..seaplayer import SeaPlayer
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
    
    def __init__(
        self,
        app: SeaPlayer,
        pl: PluginLoader,
        info: PluginInfo
    ) -> None: ...

    def on_init(self) -> None: ...
    def on_run(self) -> None: ...
    async def on_compose(self) -> None: ...
    async def on_quit(self) -> None: ...

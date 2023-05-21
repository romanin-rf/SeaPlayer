from pydantic import BaseModel
# > Typing
from typing import Optional
# > Local Import's
from ..seaplayer import SeaPlayer

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
    
    def __init__(self, app: SeaPlayer, pl, info) -> None: ...
    async def on_init(self) -> None: ...
    async def on_start(self) -> None: ...
    async def on_quit(self) -> None: ...

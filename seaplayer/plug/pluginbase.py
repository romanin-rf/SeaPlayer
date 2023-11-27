from pydantic import BaseModel
# > Local Import's
from typing import Optional

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
    def __init_repr__(self) -> str:
        return f"[green]{self.info.name}[/] ({repr(self.info.name_id)}) [#00ffee]v{self.info.version}[/#00ffee] [yellow]is initialized[/yellow]!"
    
    def __init__(self, app, pl, info: PluginInfo) -> None:
        self.app = app
        self.pl = pl
        self.info = info
        # > Logs
        self.app.info(self.__init_repr__())
    
    def on_init(self): pass
    def on_run(self): pass
    async def on_compose(self): pass
    async def on_quit(self): pass

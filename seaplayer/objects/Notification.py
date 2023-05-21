from textual.widgets import Static
# > Typing
from typing import Literal


class Nofy(Static):
    def __init__(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top",
        **kwargs
    ) -> None:
        super().__init__(text, **kwargs)
        self.life_time = life_time
        self.styles.dock = dosk
    
    def on_mount(self) -> None: self.set_timer(self.life_time, self.remove)
    async def on_click(self) -> None: await self.remove()

class CallNofy(Static):
    def __init__(
        self,
        text: str,
        dosk: Literal["bottom", "left", "right", "top"]="top",
        **kwargs
    ) -> None:
        super().__init__(text, **kwargs)
        self.styles.dock = dosk
from textual.widgets import Button
# > Typing
from typing import Callable, Awaitable

# ! Clikable Button Class
class ClikableButton(Button):
    def __init__(self, label: str, on_click: Callable[[], Awaitable[None]], *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.__on_click_method = on_click
    
    async def on_click(self, *args, **kwargs) -> None:
        await self.__on_click_method()
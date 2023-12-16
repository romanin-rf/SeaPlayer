import asyncio
from rich.text import TextType
from textual.widgets import Button
# > Typing
from typing import Optional, Callable, Awaitable

# ! Clikable Button Class
class ClikableButton(Button):
    def __init__(self, label: str, on_click: Callable[[], Awaitable[None]], *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.__on_click_method = on_click
    
    async def on_click(self, *args, **kwargs) -> None:
        await self.__on_click_method()

# ! Wait Button Click
class WaitButton(Button):
    def __init__(self, label: Optional[TextType]=None, queue_max_size: int=1, *args, **kwargs) -> None:
        super().__init__(label, *args, **kwargs)
        self.__wait_queue: asyncio.Queue[bool] = asyncio.Queue(queue_max_size)
    
    async def on_click(self, *args, **kwargs) -> None:
        await self.__wait_queue.put(True)
    
    async def wait_click(self) -> bool:
        return await self.__wait_queue.get()
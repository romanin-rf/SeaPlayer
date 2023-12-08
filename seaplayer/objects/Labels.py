from textual.widgets import Label
from rich.segment import Segments, Segment
from rich.style import Style
# > Typing
from typing import Optional

# ! Main Class
class FillLabel(Label):
    def _gen(self) -> Segments:
        return Segments([Segment(self.__chr, self.__style) for i in range((self.size[0] * self.size[1]))])
    
    def __init__(
        self,
        char: str="-",
        style: Optional[Style]=None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.__chr = char[:1]
        self.__style = style
        self.update(self._gen())
    
    async def on_resize(self) -> None:
        self.update(self._gen())
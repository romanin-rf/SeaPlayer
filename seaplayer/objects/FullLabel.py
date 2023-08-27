from textual.widgets import Label

# ! Main Class
class FullLabel(Label):
    def _gen(self) -> str:
        return self._chr * (self.size[0] * self.size[1])
    
    def __init__(self, char: str="-") -> None:
        super().__init__(classes="full-label")
        self._chr = char
        self.update(self._gen())
    
    async def on_resize(self) -> None:
        self.update(self._gen())
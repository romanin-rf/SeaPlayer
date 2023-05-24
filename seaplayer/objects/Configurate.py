from textual.containers import ScrollableContainer, Container
# > Typing
from typing import Optional, Union


class ConfigurateListItem(Container):
    def __init__(
        self,
        *children,
        title: str="",
        desc: str="",
        width: Union[int, str]="1fr",
        height: Union[int, str]="1fr",
        **kwargs
    ):
        kwargs["classes"] = "configurate-list-view-item"
        super().__init__(*children, **kwargs)
        self.border_title = title
        self.border_subtitle = desc
        self.styles.width = width
        self.styles.height = height
    
    async def updating(self, title: Optional[str]="", desc: Optional[str]="") -> None:
        if title is not None: self.border_title = title
        if desc is not None: self.border_subtitle = desc

class ConfigurateList(ScrollableContainer):
    def __init__(self, *children, **kwargs):
        kwargs["classes"] = "configurate-list-view"
        super().__init__(*children, **kwargs)
        self.border_title = "Configurate"
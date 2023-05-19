from textual.widgets import ListItem, ListView
# > Typing
from typing import Optional


class ConfigurateListItem(ListItem):
    def __init__(
        self,
        *children,
        title: str="",
        desc: str="",
        **kwargs
    ):
        kwargs["classes"] = "configurate-list-view-item"
        super(ConfigurateListItem, self).__init__(*children, **kwargs)
        self.border_title = title
        self.border_subtitle = desc
    
    async def updating(self, title: Optional[str]="", desc: Optional[str]="") -> None:
        if title is not None: self.border_title = title
        if desc is not None: self.border_subtitle = desc

class ConfigurateListView(ListView):
    def __init__(self, *children, **kwargs):
        kwargs["classes"] = "configurate-list-view"
        super().__init__(*children, **kwargs)
        self.border_title = "Configurate"
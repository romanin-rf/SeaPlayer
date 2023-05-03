import os
import base64
import platform
# > Graphics
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Header, Footer, Input
# > Local Imports
from .config import SeaPlayerConfig
from .objects import ConfigurateListView, ConfigurateListItem

# ! Constants
TEXT = b'CkFuIGVycm9yIGhhcyBvY2N1cnJlZC4gVG8gY29udGludWU6CgpQcmVzcyBFbnRlciB0byByZXR1cm4gdG8ge3N5c3RlbX0sIG9yCgpQcmVzcyBDVFJMK0FMVCtERUwgdG8gcmVzdGFydCB5b3VyIGNvbXB1dGVyLiBJZiB5b3UgZG8gdGhpcywKeW91IHdpbGwgbG9zZSBhbnkgdW5zYXZlZCBpbmZvcm1hdGlvbiBpbiBhbGwgb3BlbiBhcHBsaWNhdGlvbnMuCgpFcnJvcjogMEUgOiAwMTZGIDogQkZGOUIzRDQK'
TEXT = base64.b64decode(TEXT).decode(errors="ignore").format(system=platform.system())
UNKNOWN_OPEN_KEY = base64.b64decode(b"Yg==").decode(errors="ignore")

# ! Screens
class Unknown(Screen):
    """This Unknown screen."""
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Static(f" {platform.system()} ", id="unknown-title")
        yield Static(TEXT)
        yield Static("Press any key to continue [blink]_[/]", id="unknown-any-key")

class Configurate(Screen):
    """This Configurate Menu screen."""
    BINDINGS = [("escape", "app.pop_screen", "Back")]
    
    def compose(self) -> ComposeResult:
        self.app_config: SeaPlayerConfig = self.app.config
        
        yield Header()
        yield ConfigurateListView(
            ConfigurateListItem("(Key): QUIT", "Сlose the app."),
            ConfigurateListItem("(Key): Rewind Forward", "Forwards rewinding."),
            ConfigurateListItem("(Key): Rewind Back", "Backwards rewinding."),
            ConfigurateListItem("(Key): Volume +", "Turn up the volume."),
            ConfigurateListItem("(Key): Volume -", "Turn down the volume.")
        )
        yield Footer()
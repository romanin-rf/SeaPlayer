import os
import base64
import platform
# > Graphics
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, ListView, ListItem, Header, Footer, Input, Label
# > Local Imports
from .config import SeaPlayerConfig
from .objects import ConfigurateListView, ConfigurateListItem, InputField

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
    
    # ! Update Placeholder from InputField
    def _upfif(self, attr_name: str) -> str:
        return "Currect: " + str(eval(f"self.app_config.{attr_name}"))
    def _generate_upfif(self, attr_name: str):
        return lambda: self._upfif(attr_name)
    
    # ! Update App Config
    async def _uac(self, attr_name: str, input: InputField, value: str) -> None:
        exec(f"self.app_config.{attr_name} = value")
    
    def _generate_uac(self, attr_name: str):
        async def an_uac(input: InputField, value: str) -> None: await self._uac(attr_name, input, value)
        return an_uac
    
    # ! Configurate Main Functions
    def compose(self) -> ComposeResult:
        self.app_config: SeaPlayerConfig = self.app.config
        
        yield Header()
        yield ConfigurateListView(
            ConfigurateListItem(
                InputField(
                    submit=self._generate_uac("key_quit"),
                    update_placeholder=self._generate_upfif("key_quit")
                ),
                title="(Key): QUIT",
                desc="Сlose the app. [red](restart required)[/]"
            ),
            ConfigurateListItem(
                InputField(
                    submit=self._generate_uac("key_rewind_forward"),
                    update_placeholder=self._generate_upfif("key_rewind_forward")
                ),
                title="(Key): Rewind Forward",
                desc="Forwards rewinding. [red](restart required)[/]"
            ),
            ConfigurateListItem(
                InputField(
                    submit=self._generate_uac("key_rewind_back"),
                    update_placeholder=self._generate_upfif("key_rewind_back")
                ),
                title="(Key): Rewind Back",
                desc="Backwards rewinding. [red](restart required)[/]"
            ),
            ConfigurateListItem(
                InputField(
                    submit=self._generate_uac("key_volume_up"),
                    update_placeholder=self._generate_upfif("key_volume_up")
                ),
                title="(Key): Volume +",
                desc="Turn up the volume. [red](restart required)[/]"
            ),
            ConfigurateListItem(
                InputField(
                    submit=self._generate_uac("key_volume_down"),
                    update_placeholder=self._generate_upfif("key_volume_down")
                ),
                title="(Key): Volume -",
                desc="Turn down the volume. [red](restart required)[/]"
            )
        )
        yield Footer()
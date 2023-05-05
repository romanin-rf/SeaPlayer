import base64
import platform
# > Graphics
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Header, Footer
# > Typing
from typing import Optional
# > Local Imports
from .types import Converter
from .modules.colorizer import richefication
from .objects import ConfigurateListView, ConfigurateListItem, InputField

# ! Constants
TEXT = b'CkFuIGVycm9yIGhhcyBvY2N1cnJlZC4gVG8gY29udGludWU6CgpQcmVzcyBFbnRlciB0byByZXR1cm4gdG8ge3N5c3RlbX0sIG9yCgpQcmVzcyBDVFJMK0FMVCtERUwgdG8gcmVzdGFydCB5b3VyIGNvbXB1dGVyLiBJZiB5b3UgZG8gdGhpcywKeW91IHdpbGwgbG9zZSBhbnkgdW5zYXZlZCBpbmZvcm1hdGlvbiBpbiBhbGwgb3BlbiBhcHBsaWNhdGlvbnMuCgpFcnJvcjogMEUgOiAwMTZGIDogQkZGOUIzRDQK'
TEXT = base64.b64decode(TEXT).decode(errors="ignore").format(system=platform.system())
UNKNOWN_OPEN_KEY = base64.b64decode(b"Yg==").decode(errors="ignore")

# ! Initializing
conv = Converter()

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
        return "Currect: " + str(eval(f"self.{attr_name}"))
    def gupfif(self, attr_name: str):
        return lambda: self._upfif(attr_name)
    
    # ! Update App Config
    async def _uac(self, attr_name: str, input: InputField, value: str) -> None:
        exec(f"self.{attr_name} = value")
    
    def guac(self, attr_name: str):
        async def an_uac(input: InputField, value: str) -> None: await self._uac(attr_name, input, value)
        return an_uac
    
    # ! Configurator Generators
    def create_configurator_type(
        self,
        attr_name: str,
        title: str="",
        desc: str="",
        _type: type=str,
        type_alias: type=str,
        restart_required: bool=True
    ) -> ConfigurateListItem:
        return ConfigurateListItem(
            InputField(
                conv=conv.gen_aio_conv(_type),
                submit=self.guac(attr_name),
                update_placeholder=self.gupfif(attr_name)
            ),
            title=title+f" ({richefication(type_alias)})",
            desc=desc+(" [red](restart required)[/]" if restart_required else "")
        )
    
    def create_configurator_keys(
        self,
        attr_name: str,
        title: str="",
        desc: str="",
        restart_required: bool=True
    ) -> ConfigurateListItem:
        return ConfigurateListItem(
            InputField(
                submit=self.guac(attr_name),
                update_placeholder=self.gupfif(attr_name)
            ),
            title=title+f" ({richefication(str)})",
            desc=desc+(" [red](restart required)[/]" if restart_required else "")
        )
    
    # ! Configurate Main Functions
    def compose(self) -> ComposeResult:
        yield Header()
        yield ConfigurateListView(
            self.create_configurator_type(
                "app.config.sound_font_path",
                "[red]{Sound}[/]: Sound Font Path",
                "Path to SF2-file.",
                conv.optional(conv.filepath), Optional[str], False
            ),
            self.create_configurator_type(
                "app.config.volume_change_percent",
                "[red]{Playback}[/]: Volume Change Percent",
                "Percentage by which the volume changes when the special keys are pressed.",
                float, float
            ),
            self.create_configurator_type(
                "app.config.rewind_count_seconds",
                "[red]{Playback}[/]: Rewind Count Seconds",
                "The value of the seconds by which the current sound will be rewound.",
                int, int
            ),
            self.create_configurator_type(
                "app.config.max_volume_percent",
                "[red]{Playback}[/]: Max Volume Percent",
                "Maximum volume value.",
                float, float
            ),
            self.create_configurator_type(
                "app.config.recursive_search",
                "[red]{Playlist}[/]: Recursive Search",
                "Recursive file search.",
                conv.boolean, bool, False
            ),
            self.create_configurator_keys("app.config.key_quit", "[red]{KEY}[/]: Quit", "Сlose the app."),
            self.create_configurator_keys("app.config.key_rewind_forward", "[red]{KEY}[/]: Rewind Forward", "Forwards rewinding."),
            self.create_configurator_keys("app.config.key_rewind_back", "[red]{KEY}[/]: Rewind Back", "Backwards rewinding."),
            self.create_configurator_keys("app.config.key_volume_up", "[red]{KEY}[/]: Volume +", "Turn up the volume."),
            self.create_configurator_keys("app.config.key_volume_down", "[red]{KEY}[/]: Volume -", "Turn down the volume.")
        )
        yield Footer()

import base64
import platform
from pathlib import Path
# > Graphics
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Header, Footer
# > Typing
from typing import Optional, Any, Tuple
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
    
    @staticmethod
    async def _conv(tp: type, value: str) -> Tuple[bool, Optional[Any]]:
        try: return True, eval("tp(value)")
        except: return False, None
    
    def _generate_conv(self, tp: type):
        async def _tp_conv(value: str): return await self._conv(tp, value)
        return _tp_conv
    
    # ! Configurator Generators
    def create_configurator_keys(
        self,
        attr_name: str,
        title: str="",
        desc: str="",
        restart_required: bool=True
    ) -> None:
        return ConfigurateListItem(
            InputField(
                submit=self._generate_uac(attr_name),
                update_placeholder=self._generate_upfif(attr_name)
            ),
            title=title,
            desc=desc+(" [red](restart required)[/]" if restart_required else "")
        )
    
    def create_configurator_type(
        self,
        attr_name: str,
        title: str="",
        desc: str="",
        _type: type=str,
        restart_required: bool=True
    ) -> None:
        return ConfigurateListItem(
            InputField(
                conv=self._generate_conv(_type),
                submit=self._generate_uac(attr_name),
                update_placeholder=self._generate_upfif(attr_name)
            ),
            title=title,
            desc=desc+(" [red](restart required)[/]" if restart_required else "")
        )
    
    @staticmethod
    def _conv_path(value: str) -> str:
        path = Path(value)
        if not(path.exists() and path.is_file()): raise FileNotFoundError(value)
        return value
    
    @staticmethod
    def _conv_optional(tp: type):
        def _m_conv_optional(value: str):
            if value.lower() != "none": return tp(value)
        return _m_conv_optional
    
    @staticmethod
    def _conv_bool(value: str):
        if value.lower() == "true": return True
        elif value.lower() == "false": return False
        else: raise TypeError(value, bool)
    
    # ! Configurate Main Functions
    def compose(self) -> ComposeResult:
        self.app_config: SeaPlayerConfig = self.app.config
        
        yield Header()
        yield ConfigurateListView(
            self.create_configurator_type(
                "sound_font_path",
                "{Sound}: Sound Font Path ([green]Path[white][[/]str[white]][/][/] [white]|[/] [blue]None[/])",
                "Path to SF2-file.", self._conv_optional(self._conv_path), False
            ),
            self.create_configurator_type(
                "volume_change_percent",
                "{Playback}: Volume Change Percent ([green]float[/])",
                "Percentage by which the volume changes when the special keys are pressed.", float
            ),
            self.create_configurator_type(
                "rewind_count_seconds",
                "{Playback}: Rewind Count Seconds ([green]int[/])",
                "The value of the seconds by which the current sound will be rewound.", int
            ),
            self.create_configurator_type(
                "max_volume_percent",
                "{Playback}: Max Volume Percent ([green]float[/])",
                "Maximum volume value.", float
            ),
            self.create_configurator_type(
                "recursive_search",
                "{Playlist}: Recursive Search ([green]bool[/])",
                "Recursive file search.", self._conv_bool
            ),
            self.create_configurator_keys("key_quit", "{Key}: QUIT ([green]str[/])", "Сlose the app."),
            self.create_configurator_keys("key_rewind_forward", "{Key}: Rewind Forward ([green]str[/])", "Forwards rewinding."),
            self.create_configurator_keys("key_rewind_back", "{Key}: Rewind Back ([green]str[/])", "Backwards rewinding."),
            self.create_configurator_keys("key_volume_up", "{Key}: Volume + ([green]str[/])", "Turn up the volume."),
            self.create_configurator_keys("key_volume_down", "{Key}: Volume - ([green]str[/])", "Turn down the volume.")
        )
        yield Footer()

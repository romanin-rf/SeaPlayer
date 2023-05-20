from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
# > Typing
from typing import Optional, Literal
# > Local Imports
from ..types import Converter
from ..modules.colorizer import richefication
from ..objects import (
    Nofy,
    InputField,
    ConfigurateList,
    ConfigurateListItem
)

# ! Vars
conv = Converter()

# ! Main Class
class Configurate(Screen):
    """This Configurate Menu screen."""
    BINDINGS = [("escape", "app.pop_screen", "Back")]
    
    # ! Nofy Functions
    def nofy(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> None:
        self.screen.mount(Nofy(text, life_time, dosk))
    
    async def aio_nofy(
        self,
        text: str,
        life_time: float=3,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> None:
        await self.screen.mount(Nofy(text, life_time, dosk))
    
    # ! Update Placeholder from InputField
    def _upfif(self, attr_name: str) -> str:
        return "Currect: " + str(eval(f"self.{attr_name}"))
    def gupfif(self, attr_name: str):
        return lambda: self._upfif(attr_name)
    
    # ! Update App Config
    async def _uac(self, attr_name: str, input: InputField, value: str) -> None:
        exec(f"self.{attr_name} = value")
        await self.aio_nofy("Saved!")
    
    def guac(self, attr_name: str):
        async def an_uac(input: InputField, value: str) -> None: await self._uac(attr_name, input, value)
        return an_uac

    # ! Configurator Generators
    def create_configurator_type(
        self,
        attr_name: str,
        group: str="Option",
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
            title="[red]{"+group+"}[/]: "+title+f" ({richefication(type_alias)})",
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
            title="[red]{Key}[/]: "+title+f" ({richefication(str)})",
            desc=desc+(" [red](restart required)[/]" if restart_required else "")
        )
    
    # ! Configurate Main Functions # 
    def compose(self) -> ComposeResult:
        yield Header()
        yield ConfigurateList(
            self.create_configurator_type(
                "app.config.sound_font_path",
                "Sound", "Sound Font Path",
                "Path to SF2-file.",
                conv.optional(conv.filepath), Optional[str], False
            ),
            self.create_configurator_type(
                "app.config.image_update_method",
                "Image", "Image Update Method",
                "The name of the picture update option.",
                conv.literal_string("sync", "async"), Literal["sync", "async"]
            ),
            self.create_configurator_type(
                "app.config.image_resample_method",
                "Image", "Image Resample Method",
                "Method for reducing/increasing the number of pixels.",
                conv.literal_string("nearest", "bilinear", "bicubic", "lanczos", "hamming", "box"), Literal["nearest", "bilinear", "bicubic", "lanczos", "hamming", "box"]
            ),
            self.create_configurator_type(
                "app.config.volume_change_percent",
                "Playback", "Volume Change Percent",
                "Percentage by which the volume changes when the special keys are pressed.",
                float, float
            ),
            self.create_configurator_type(
                "app.config.rewind_count_seconds",
                "Playback", "Rewind Count Seconds",
                "The value of the seconds by which the current sound will be rewound.",
                int, int
            ),
            self.create_configurator_type(
                "app.config.max_volume_percent",
                "Playback", "Max Volume Percent",
                "Maximum volume value.",
                float, float
            ),
            self.create_configurator_type(
                "app.config.recursive_search",
                "Playlist", "Recursive Search",
                "Recursive file search.",
                conv.boolean, bool, False
            ),
            self.create_configurator_type(
                "app.config.log_menu_enable",
                "Debag", "Log Menu Enable",
                "Menu with logs for the current session.",
                conv.boolean, bool
            ),
            self.create_configurator_keys("app.config.key_quit", "Quit", "Сlose the app."),
            self.create_configurator_keys("app.config.key_rewind_forward", "Rewind Forward", "Forwards rewinding."),
            self.create_configurator_keys("app.config.key_rewind_back", "Rewind Back", "Backwards rewinding."),
            self.create_configurator_keys("app.config.key_volume_up", "Volume +", "Turn up the volume."),
            self.create_configurator_keys("app.config.key_volume_down", "Volume -", "Turn down the volume.")
        )
        yield Footer()

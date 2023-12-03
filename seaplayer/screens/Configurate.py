from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
# > Typing
try:
    from sounddevice import query_devices, query_hostapis
    INIT_SOUNDDEVICE = True
except:
    INIT_SOUNDDEVICE = False
from typing import Optional, Literal, Union, Tuple, Dict, List, Any
# > Local Imports
from ..types import Converter
from ..modules.colorizer import richefication
from ..objects import (
    Nofy,
    InputField,
    DataOptionList, DataOption,
    DataRadioSet, DataRadioButton,
    ConfigurateList, ConfigurateListItem
)

# ! Vars
conv = Converter()

# ! Functions
if INIT_SOUNDDEVICE:
    def generate_devices_options(currect: Optional[int]=None):
        hosts: List[Dict[str, Any]] = [_1 for _1 in query_hostapis()]
        devices: List[Dict[str, Any]] = [_2 for _2 in query_devices()]
        devices_options: List[DataOption] = []
        devices_options.append(DataOption("([cyan]*[/cyan]) [yellow]Auto[/yellow]", device_index=None))
        
        for device in devices:
            if device["max_output_channels"] > 0:
                try:
                    format_data = dict(
                        device_name=device["name"], 
                        device_index=device["index"],
                        hostapi_index=device["hostapi"],
                        hostapi_name=hosts[device["hostapi"]]["name"]
                    )
                    devices_options.append(
                        DataOption(
                            "([cyan]{device_index}[/cyan]) [yellow]{device_name}[/yellow] \[[green]{hostapi_name}[/green]]".format(**format_data),
                            device_index=device["index"]
                        )
                    )
                except:
                    pass
        for d in devices_options:
            if d.data["device_index"] == currect:
                d.selected = True
        return devices_options

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
    async def _auac(self, attr_name: str, input: InputField, value: str) -> None:
        exec(f"self.{attr_name} = value")
        self.app.update_bindings()
        await self.aio_nofy("Saved!")
    
    def _caa(self, attr_name: str, value: str) -> None:
        exec(f"self.{attr_name} = value")
        self.app.update_bindings()
        self.nofy("Saved!")
    
    def _gaa(self, attr_name: str) -> Any:
        return eval(f"self.{attr_name}")
    
    if INIT_SOUNDDEVICE:
        def gucsdi(self):
            async def n_ucsdi(option: DataOption) -> None:
                self.app.config.output_sound_device_id = option.data.get("device_index", None)
                await self.aio_nofy("Saved!")
            return n_ucsdi
    
    def guac(self, attr_name: str):
        async def an_uac(input: InputField, value: str) -> None:
            await self._auac(attr_name, input, value)
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
            title="[red]{"+group+"}[/red]: "+f"{title} ({richefication(type_alias)})",
            desc=desc+(" [red](restart required)[/red]" if restart_required else ""),
            height=5
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
            title="[red]{Key}[/red]: "+f"{title} ({richefication(str)})",
            desc=desc+(" [red](restart required)[/red]" if restart_required else ""),
            height=5
        )
    
    def create_configurator_literal(
        self,
        attr_name: str,
        values: List[Union[Any, Tuple[Any, str]]],
        group: str="Option",
        title: str="",
        desc: str="",
        restart_required: bool=True
    ) -> ConfigurateListItem:
        on_changed_method = lambda v: self._caa(attr_name, v)
        default_value = [v[0] if isinstance(v, tuple) else v for v in values].index(self._gaa(attr_name))
        buttons = []
        for idx, d in enumerate(values):
            drb = \
                DataRadioButton(d[0], idx==default_value, d[1]) \
            if isinstance(d, tuple) else \
                DataRadioButton(d, idx==default_value)
            buttons.append(drb)
        return ConfigurateListItem(
            DataRadioSet(on_changed_method, *buttons),
            title="[red]{"+group+"}[/red]: "+title,
            desc=desc + " [red](restart required)[/red]" if restart_required else "",
            height=len(values)+4
        )
    
    if INIT_SOUNDDEVICE:
        def create_configurator_sound_devices(self):
            dos = generate_devices_options(self.app.config.output_sound_device_id)
            options_list = DataOptionList(
                *dos,
                group="SoundDevicesSelect",
                after_selected=self.gucsdi()
            )
            return ConfigurateListItem(
                options_list,
                title="[red]{Sound}[/]: Output Sound Device",
                desc="Select the device that SeaPlayer will work with. [red](restart required)[/red]",
                height=len(dos)+4
            )
    
    # ! Configurate Main Functions
    def compose(self) -> ComposeResult:
        yield Header()
        with ConfigurateList():
            yield self.create_configurator_type(
                "app.config.sound_font_path",
                "Sound", "Sound Font Path",
                "Path to SF2-file.",
                conv.optional(conv.filepath), Optional[str], False
            )
            if INIT_SOUNDDEVICE:
                yield self.create_configurator_sound_devices()
            yield self.create_configurator_literal(
                "app.config.image_update_method",
                [
                    ("sync", "Synchronously"),
                    ("async", "Asynchronously")
                ],
                "Image", "Image Update Method",
                "The name of the picture update option."
            )
            yield self.create_configurator_literal(
                "app.config.image_resample_method",
                [
                    ("nearest", "Nearest"),
                    ("bilinear", "Bilinear"),
                    ("bicubic", "Bicubic"),
                    ("lanczos", "Lanczos"),
                    ("hamming", "Hamming"),
                    ("box", "Boxing"),
                ],
                "Image", "Image Resample Method",
                "Method for reducing/increasing the number of pixels."
            )
            yield self.create_configurator_type(
                "app.config.volume_change_percent",
                "Playback", "Volume Change Percent",
                "Percentage by which the volume changes when the special keys are pressed.",
                float, float, False
            )
            yield self.create_configurator_type(
                "app.config.rewind_count_seconds",
                "Playback", "Rewind Count Seconds",
                "The value of the seconds by which the current sound will be rewound.",
                int, int, False
            )
            yield self.create_configurator_type(
                "app.config.max_volume_percent",
                "Playback", "Max Volume Percent",
                "Maximum volume value.",
                float, float, False
            )
            yield self.create_configurator_literal(
                "app.config.recursive_search",
                [(True, "On"), (False, "Off")],
                "Playlist", "Recursive Search",
                "Recursive file search.", False
            )
            yield self.create_configurator_literal(
                "app.config.log_menu_enable",
                [(True, "On"), (False, "Off")],
                "Debag", "Log Menu Enable",
                "Menu with logs for the current session.", False
            )
            yield self.create_configurator_keys("app.config.key_quit", "Quit", "Сlose the app.", False)
            yield self.create_configurator_keys("app.config.key_rewind_forward", "Rewind Forward", "Forwards rewinding.", False)
            yield self.create_configurator_keys("app.config.key_rewind_back", "Rewind Back", "Backwards rewinding.", False)
            yield self.create_configurator_keys("app.config.key_volume_up", "Volume +", "Turn up the volume.", False)
            yield self.create_configurator_keys("app.config.key_volume_down", "Volume -", "Turn down the volume.", False)
        yield Footer()

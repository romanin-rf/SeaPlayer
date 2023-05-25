import os
import glob
import asyncio
# > Graphics
from textual import on
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label, Button
# > Image Works
from PIL import Image
# > Typing
from typing import Optional, Literal, Tuple, List, Type
# > Local Imports
from .config import *
from .plug import PluginLoader
from .codeсbase import CodecBase
from .screens import Unknown, Configurate, UNKNOWN_OPEN_KEY
from .codecs import codecs
from .functions import (
    aiter,
    check_status,
    rich_exception,
    image_from_bytes,
    get_sound_basename
)
from .objects import (
    Nofy,
    LogMenu,
    CallNofy,
    InputField,
    MusicListView,
    AsyncImageLabel,
    MusicListViewItem,
    StandartImageLabel,
    IndeterminateProgress
)
from .units import (
    __title__,
    __version__,
    __author__,
    __email__,
    __url__,
    CSS_LOCALDIR,
    CONFIG_FILEPATH,
    ASSETS_DIRPATH,
    IMGPATH_IMAGE_NOT_FOUND,
    RESAMPLING_SAFE,
    LOCALDIR
)

# ! Main Functions
def build_bindings(config: SeaPlayerConfig):
    yield Binding(config.key_quit, "quit", "Quit")
    yield Binding("c,с", "push_screen('configurate')", "Configurate")
    if config.log_menu_enable:
        yield Binding("l,д", "app.toggle_class('.log-menu', '-hidden')", 'Logs')
    yield Binding(config.key_rewind_back, "minus_rewind", f"Rewind -{config.rewind_count_seconds} sec")
    yield Binding(config.key_rewind_forward, "plus_rewind", f"Rewind +{config.rewind_count_seconds} sec")
    yield Binding(config.key_volume_down, "minus_volume", f"Volume -{round(config.volume_change_percent*100)}%")
    yield Binding(config.key_volume_up, "plus_volume", f"Volume +{round(config.volume_change_percent*100)}%")
    yield Binding("ctrl+s", "screenshot", "Screenshot")
    yield Binding(UNKNOWN_OPEN_KEY, "push_screen('unknown')", "None", show=False)

# ! Main
class SeaPlayer(App):
    # ! Textual Configuration
    TITLE = f"{__title__} v{__version__}"
    CSS_PATH = [
        os.path.join(CSS_LOCALDIR, "seaplayer.css"),
        os.path.join(CSS_LOCALDIR, "configurate.css"),
        os.path.join(CSS_LOCALDIR, "unknown.css"),
        os.path.join(CSS_LOCALDIR, "objects.css")
    ]
    SCREENS = {
        "unknown": Unknown(id="screen_unknown"),
        "configurate": Configurate(id="screen_configurate")
    }
    
    # ! SeaPlayer Configuration
    config = SeaPlayerConfig(CONFIG_FILEPATH)
    max_volume_percent: float = config.max_volume_percent
    
    # ! Textual Keys Configuration
    BINDINGS = list(build_bindings(config))
    
    # ! Template Configuration
    currect_sound_uuid: Optional[str] = None
    currect_sound: Optional[CodecBase] = None
    currect_volume = 1.0
    last_playback_status: Optional[Literal["Stoped", "Playing", "Paused"]] = None
    playback_mode: int = 0
    playback_mode_blocked: bool = False
    last_paths_globalized: List[str] = []
    started: bool = True
    
    # ! Codecs Configuration
    CODECS: List[Type[CodecBase]] = [ *codecs ]
    CODECS_KWARGS: Dict[str, Any] = {
        "sound_fonts_path": config.sound_font_path,
        "sound_device_id": config.output_sound_device_id
    }
    
    # ! Init Objects
    log_menu = LogMenu(enable_logging=config.log_menu_enable, wrap=True, highlight=True, markup=True)
    
    # ! Log Functions
    info = log_menu.info
    error = log_menu.error
    warn = log_menu.warn

    # ! App Init
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.plugin_loader = PluginLoader(self)
        self.plugin_loader.on_init()
    
    # ! Inherited Functions
    async def action_push_screen(self, screen: str) -> None:
        if self.SCREENS[screen].id != self.screen.id:
            await super().action_push_screen(screen)
    
    # ! Nofy's
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
    
    def callnofy(
        self,
        text: str,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> CallNofy:
        cn = CallNofy(text, dosk)
        self.screen.mount(cn)
        return cn
    
    async def aio_callnofy(
        self,
        text: str,
        dosk: Literal["bottom", "left", "right", "top"]="top"
    ) -> CallNofy:
        cn = CallNofy(text, dosk)
        await self.screen.mount(cn)
        return cn

    # ! Functions, Workers and other...
    def gcs(self) -> Optional[CodecBase]:
        if (self.currect_sound is None) and (self.currect_sound_uuid is not None):
            self.currect_sound = self.music_list_view.music_list.get(self.currect_sound_uuid)
        return self.currect_sound
    
    async def aio_gcs(self):
        if (self.currect_sound is None) and (self.currect_sound_uuid is not None):
            self.currect_sound = await self.music_list_view.music_list.aio_get(self.currect_sound_uuid)
        return self.currect_sound

    async def get_sound_seek(self) -> Tuple[str, Optional[float], Optional[float]]:
        if (sound:=await self.aio_gcs()) is not None:
            pos = sound.get_pos()
            minutes, seconds = round(pos // 60), round(pos % 60)
            return f"{minutes}:{str(seconds).rjust(2,'0')} | {str(round(sound.get_volume()*100)).rjust(3)}%", pos, sound.duration
        return "0:00 |   0%", None, None
    
    def get_sound_selected_label_text(self) -> str:
        if (sound:=self.gcs()) is not None:
            return f"({check_status(sound)}): {get_sound_basename(sound)}"
        return "<sound not selected>"
    
    async def aio_get_sound_selected_label_text(self) -> str:
        if (sound:=await self.aio_gcs()) is not None:
            return f"({check_status(sound)}): {get_sound_basename(sound)}"
        return "<sound not selected>"
    
    def gpms(self, modes: Tuple[str, str, str]=("(MODE): PLAY", "(MODE): REPLAY SOUND", "(MODE): REPLAY LIST")) -> str: return modes[self.playback_mode]
    def switch_playback_mode(self) -> None:
        if self.playback_mode == 2: self.playback_mode = 0
        else: self.playback_mode += 1
    
    async def update_loop_playback(self) -> None:
        while self.started:
            if (sound:=await self.aio_gcs()) is not None:
                status = check_status(sound)
                if (self.last_playback_status is not None) and (self.last_playback_status != status):
                    self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
                
                if (status == "Stoped") and (self.last_playback_status == "Playing"):
                    if self.playback_mode == 1:
                        sound.play()
                        self.info(f"Replay sound: {repr(sound)}")
                    elif self.playback_mode == 2:
                        if (sound:=await self.set_sound_for_playback(sound_uuid:=await self.music_list_view.aio_get_next_sound_uuid(self.currect_sound_uuid), True)) is not None:
                            self.playback_mode_blocked = True
                            await self.music_list_view.aio_select_list_item_from_sound_uuid(sound_uuid)
                            sound.play()
                            self.info(f"Playing the next sound: {repr(sound)}")
                
                self.last_playback_status = status
            await asyncio.sleep(0.2)
    
    def compose(self) -> ComposeResult:     
        # * Other
        self.info("--- [pink]SeaPlayer.compose[/pink] [green]Starting[/green] ---")
        self.info(f"{__title__} v{__version__} from {__author__} ({__email__})")
        self.info(f"Source          : {__url__}")
        self.info(f"Codecs          : {repr(self.CODECS)}")
        self.info(f"Config Path     : {repr(self.config.filepath)}")
        self.info(f"CSS Dirpath     : {repr(CSS_LOCALDIR)}")
        self.info(f"Assets Dirpath  : {repr(ASSETS_DIRPATH)}")
        self.info(f"Codecs Kwargs   : {repr(self.CODECS_KWARGS)}")
        self.info(f"Sound Device ID : {repr(self.config.output_sound_device_id)}")
        
        
        # * Play Screen
        self.music_play_screen = Static(classes="screen-box")
        self.music_play_screen.border_title = "Player"
        
        # * Image Object Init
        self.music_selected_label = Label(self.get_sound_selected_label_text(), classes="music-selected-label")
        if self.config.image_update_method == "sync":
            self.music_image = StandartImageLabel(Image.open(IMGPATH_IMAGE_NOT_FOUND), resample=RESAMPLING_SAFE[self.config.image_resample_method])
        elif self.config.image_update_method == "async":
            self.music_image = AsyncImageLabel(Image.open(IMGPATH_IMAGE_NOT_FOUND), resample=RESAMPLING_SAFE[self.config.image_resample_method])
        else:
            raise RuntimeError("The configuration 'image_update_method' is incorrect.")
        self.info(f"The picture from the media file is rendered using the {repr(self.config.image_update_method)} method.")
        
        # * Compositions Screen
        self.music_list_screen = Static(classes="screen-box")
        self.music_list_screen.border_title = "Playlist"
        
        self.music_list_view = MusicListView()
        
        async def _spm(input: InputField, value: Any) -> None: await self.submit_plus_sound(value)
        self.music_list_add_input = InputField(submit=_spm, placeholder="Filepath / Search Mask", classes="music-list-screen-add-input")
        
        # * Adding
        yield Header()
        with self.music_play_screen:
            with Vertical():
                with Static(classes="player-visual-panel"):
                    yield self.music_image
                with Static(classes="player-contol-panel"):
                    yield self.music_selected_label
                    yield IndeterminateProgress(getfunc=self.get_sound_seek)
                    with Horizontal(classes="box-buttons-sound-control"):
                        yield Button("Play/Stop", id="button-play-stop", variant="warning", classes="button-sound-control")
                        yield Static(classes="pass-one-width")
                        yield Button("Pause/Unpause", id="button-pause-unpause", variant="success", classes="button-sound-control")
                        yield Static(classes="pass-one-width")
                        yield Button(self.gpms(), id="switch-playback-mode", variant="primary", classes="button-sound-control")
        with self.music_list_screen:
            yield self.music_list_view
            yield self.music_list_add_input
        if self.config.log_menu_enable:
            yield self.log_menu
        yield Footer()
        
        self.run_worker(
            self.update_loop_playback,
            name="PLAYBACK_CONTROLLER",
            group="CONTROL_UPDATER-LOOP",
            description="Control of playback modes and status updates."
        )
        self.run_worker(
            self.plugin_loader.on_compose,
            name="ON_COMPOSE",
            group="PluginLoader",
            description="<method PluginLoader.on_compose>"
        )
        self.info("--- [pink]SeaPlayer.compose[/pink] [red]Starting[/red] ---")
    
    async def add_sounds_to_list(self) -> None:
        added_oks = 0
        loading_nofy = await self.aio_callnofy(
            f"Found [cyan]{len(self.last_paths_globalized)}[/cyan] values. Loading..."
        )
        async for path in aiter(self.last_paths_globalized):
            sound = None
            async for codec in aiter(self.CODECS):
                try:
                    if await codec.aio_is_this_codec(path):
                        if not hasattr(codec, "__aio_init__"):
                            try:
                                sound = codec(path, **self.CODECS_KWARGS)
                            except Exception as e:
                                self.error(rich_exception(e))
                                sound = None
                        else:
                            try:
                                sound: CodecBase = await codec.__aio_init__(path, **self.CODECS_KWARGS)
                            except Exception as e:
                                self.error(rich_exception(e))
                                sound = None
                        if sound is not None:
                            if not await self.music_list_view.music_list.aio_exists_sha1(sound):
                                await self.music_list_view.aio_add_sound(sound)
                                self.info(f"Song added: {repr(sound)}")
                                added_oks += 1
                                break
                except FileNotFoundError:
                    self.error(f"The file does not exist or is a directory: {repr(path)}")
                    break
                except Exception as e:
                    self.error(rich_exception(e))
            if sound is None:
                self.error(f"The sound could not be loaded: {repr(path)}")
        await loading_nofy.remove()
        self.info(f"Added [cyan]{added_oks}[/cyan] songs!")
        await self.aio_nofy(f"Added [cyan]{added_oks}[/cyan] songs!")
    
    async def currect_sound_stop(self, sound: Optional[CodecBase]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Stoped"
            sound.stop()
    
    async def currect_sound_play(self, sound: Optional[CodecBase]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Playing"
            sound.play()
    
    async def currect_sound_pause(self, sound: Optional[CodecBase]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Paused"
            sound.pause()
    
    async def currect_sound_unpause(self, sound: Optional[CodecBase]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Playing"
            sound.unpause()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "switch-playback-mode":
            self.switch_playback_mode()
            event.button.label = self.gpms()
    
    @on(Button.Pressed, "#button-pause-unpause")
    async def bp_pause_unpause(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if sound.playing:
                if sound.paused: await self.currect_sound_unpause(sound)
                else: await self.currect_sound_pause(sound)
            self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
    
    @on(Button.Pressed, "#button-play-stop")
    async def bp_play_stop(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if sound.playing: await self.currect_sound_stop(sound)
            else: await self.currect_sound_play(sound)
            self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
    
    async def submit_plus_sound(self, value: str) -> None:
        if value.replace(" ", "") != "":
            try: self.last_paths_globalized = glob.glob(value, recursive=self.config.recursive_search)
            except: self.last_paths_globalized = [ value ]
            self.info(f"Submit 'plus_sound' values: {repr(self.last_paths_globalized)}")
            if len(self.last_paths_globalized) > 0:
                self.run_worker(
                    self.add_sounds_to_list,
                    name="ADD_SOUND",
                    group="PLAYLIST_UPDATE",
                    description="The process of adding sounds to a playlist."
                )
    
    async def set_sound_for_playback(
        self,
        sound_uuid: Optional[str],
        playback_mode_blocked: Optional[bool]=None
    ) -> Optional[CodecBase]:
        if playback_mode_blocked is not None:
            self.playback_mode_blocked = playback_mode_blocked
        if sound_uuid is not None:
            if not self.playback_mode_blocked:
                if (sound:=await self.aio_gcs()) is not None:
                    self.last_playback_status = "Stoped"
                    sound.stop()
            self.playback_mode_blocked = False
            
            self.currect_sound_uuid = sound_uuid
            if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                sound.set_volume(self.currect_volume)
                await self.music_image.update_image(image_from_bytes(sound.icon_data))
                self.info(f"A new sound has been selected: {repr(sound)}")
            self.currect_sound = sound
            self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
            return sound
    
    async def on_list_view_selected(self, selected: MusicListView.Selected):
        if isinstance(selected.item, MusicListViewItem):
            await self.set_sound_for_playback(getattr(selected.item, "sound_uuid", None))
    
    async def action_plus_rewind(self):
        if (sound:=await self.aio_gcs()) is not None:
            sound.set_pos(sound.get_pos()+self.config.rewind_count_seconds)
    
    async def action_minus_rewind(self):
        if (sound:=await self.aio_gcs()) is not None:
            sound.set_pos(sound.get_pos()-self.config.rewind_count_seconds)
    
    async def action_plus_volume(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if (vol:=round(sound.get_volume()+self.config.volume_change_percent, 2)) <= self.max_volume_percent:
                self.currect_volume = vol
                sound.set_volume(vol)
    
    async def action_minus_volume(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if (vol:=round(sound.get_volume()-self.config.volume_change_percent, 2)) >= 0:
                self.currect_volume = vol
                sound.set_volume(vol)
    
    async def action_screenshot(self) -> None:
        path = self.save_screenshot(path=LOCALDIR)
        self.info(f"Screenshot saved to: {repr(path)}")
        await self.aio_nofy(f"Screenshot saved to: [green]{repr(path)}[/]")
    
    async def action_quit(self):
        self.started = False
        if (sound:=await self.aio_gcs()) is not None:
            sound.unpause()
            sound.stop()
            await self.plugin_loader.on_quit()
        return await super().action_quit()

    def run(self, *args, **kwargs):
        self.plugin_loader.on_run()
        super().run(*args, **kwargs)

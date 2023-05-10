import os
import sys
import glob
import asyncio
# > Sound Works
from playsoundsimple import Sound
from playsoundsimple.units import SOUND_FONTS_PATH
# > Graphics
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label, Input, Button
from textual.binding import Binding
# > Typing
from typing import Optional, Literal, Tuple, List
# > Local Imports
from .objects import *
from .config import *
from .screens import Unknown, UNKNOWN_OPEN_KEY, Configurate

# ! Metadata
__title__ = "SeaPlayer"
__version__ = "0.3.3"
__author__ = "Romanin"
__email__ = "semina054@gmail.com"
__url__ = "https://github.com/romanin-rf/SeaPlayer"

# ! Contains
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'): LOCALDIR = os.path.dirname(sys.executable)
else: LOCALDIR = os.path.dirname(os.path.dirname(__file__))

CONFIG_PATH = os.path.join(LOCALDIR, "config.properties")
CSS_LOCALDIR = os.path.join(os.path.dirname(__file__), "css")

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
    config = SeaPlayerConfig(CONFIG_PATH)
    
    max_volume_percent: float = config.max_volume_percent
    
    # ! Textual Keys Configuration
    BINDINGS = [
        Binding(key=config.key_quit, action="quit", description="Quit"),
        Binding(key=UNKNOWN_OPEN_KEY, action="push_screen('unknown')", description="None", show=False),
        Binding(key="c,с", action="push_screen('configurate')", description="Configurate"),
        Binding(key=config.key_rewind_back, action="minus_rewind", description=f"Rewind -{config.rewind_count_seconds} sec"),
        Binding(key=config.key_rewind_forward, action="plus_rewind", description=f"Rewind +{config.rewind_count_seconds} sec"),
        Binding(key=config.key_volume_down, action="minus_volume", description=f"Volume -{round(config.volume_change_percent*100)}%"),
        Binding(key=config.key_volume_up, action="plus_volume", description=f"Volume +{round(config.volume_change_percent*100)}%"),
        Binding(key="ctrl+s", action="screenshot", description="Screenshot")
    ]
    
    # ! Template Configuration
    currect_sound_uuid: Optional[str] = None
    currect_sound: Optional[Sound] = None
    currect_volume = 1.0
    last_playback_status: Optional[Literal["Stoped", "Playing", "Paused"]] = None
    playback_mode: int = 0
    playback_mode_blocked: bool = False
    last_paths_globalized: List[str] = []
    started: bool = True
    
    # ! Inherited Functions
    async def action_push_screen(self, screen: str) -> None:
        if self.SCREENS[screen].id != self.screen.id:
            await super().action_push_screen(screen)
    
    # ! Functions, Workers and other...
    def gcs(self) -> Optional[Sound]:
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
                    if self.playback_mode == 1: sound.play()
                    elif self.playback_mode == 2:
                        if (sound:=await self.set_sound_for_playback(sound_uuid:=await self.music_list_view.aio_get_next_sound_uuid(self.currect_sound_uuid), True)) is not None:
                            self.playback_mode_blocked = True
                            await self.music_list_view.aio_select_list_item_from_sound_uuid(sound_uuid)
                            sound.play()
                
                self.last_playback_status = status
            await asyncio.sleep(0.33)
    
    def compose(self) -> ComposeResult:
        # * Play Screen
        self.music_play_screen = Static(classes="screen-box")
        self.music_play_screen.border_title = "Player"
        
        self.music_selected_label = Label(self.get_sound_selected_label_text(), classes="music-selected-label")
        if self.config.image_update_method == "sync":
            self.music_image = StandartImageLabel()
        elif self.config.image_update_method == "async":
            self.music_image = AsyncImageLabel()
        else:
            raise RuntimeError("The configuration 'image_update_method' is incorrect.")
        
        # * Compositions Screen
        self.music_list_screen = Static(classes="screen-box")
        self.music_list_screen.border_title = "Playlist"
        
        self.music_list_view = MusicListView()
        self.music_list_add_input = Input(placeholder="FilePath", classes="music-list-screen-add-input")
        
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
            with Horizontal(classes="music-list-screen-add-box"):
                yield self.music_list_add_input
                yield Button("+", id="plus-sound", variant="error", classes="music-list-screen-add-button")
        yield Footer()
        
        self.run_worker(
            self.update_loop_playback,
            name="PLAYBACK_CONTROLLER",
            group="CONTROL_UPDATER-LOOP",
            description="Control of playback modes and status updates."
        )
    
    async def add_sounds_to_list(self) -> None:
        async for path in aiter(self.last_paths_globalized):
            try:
                if await aio_is_midi_file(path):
                    if self.config.sound_font_path is not None: sfp = self.config.sound_font_path
                    else: sfp = SOUND_FONTS_PATH
                    sound = Sound.from_midi(path, path_sound_fonts=sfp)
                else: sound = Sound(path)
            except: sound = None
            
            if sound is not None:
                if not await self.music_list_view.music_list.aio_exists_sha1(sound):
                    await self.music_list_view.aio_add_sound(sound)
    
    async def currect_sound_stop(self, sound: Optional[Sound]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Stoped"
            sound.stop()
    
    async def currect_sound_play(self, sound: Optional[Sound]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Playing"
            sound.play()
    
    async def currect_sound_pause(self, sound: Optional[Sound]=None):
        if sound is None: sound = await self.aio_gcs()
        if sound is not None:
            self.last_playback_status = "Paused"
            sound.pause()
    
    async def currect_sound_unpause(self, sound: Optional[Sound]=None):
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
    
    @on(Button.Pressed, "#plus-sound")
    async def bp_plus_sound(self) -> None:
        path = self.music_list_add_input.value
        self.music_list_add_input.value = ""
        
        if path.replace(" ", "") != "":
            try: self.last_paths_globalized = glob.glob(path, recursive=self.config.recursive_search)
            except: self.last_paths_globalized = []
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
    ) -> Optional[Sound]:
        if playback_mode_blocked is not None: self.playback_mode_blocked = playback_mode_blocked
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
        self.save_screenshot(path=LOCALDIR)
    
    async def action_quit(self):
        self.started = False
        if (sound:=await self.aio_gcs()) is not None:
            sound.unpause()
            sound.stop()
        return await super().action_quit()

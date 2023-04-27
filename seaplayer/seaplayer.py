import os
import sys
import json
import asyncio
from pathlib import Path
# > Sound Works
from playsoundsimple import Sound
from playsoundsimple.Units import SOUND_FONTS_PATH
# > Graphics
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label, Input, Button
from textual.binding import Binding
# > Typing
from typing import Optional, Literal, Dict, Tuple, Any
# > Local Imports
from .objects import *

# ! Metadata
__title__ = "SeaPlayer"
__version__ = "0.2.6"
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Contains
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'): LOCALDIR = os.path.dirname(sys.executable)
else: LOCALDIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(LOCALDIR, "config.json")

# ! Config Class
class SeaPlayerConfig:
    @staticmethod
    def load(filepath: Path, default: Dict[str, Any]) -> Dict[str, Any]:
        with open(filepath) as file:
            try: return json.load(file)
            except: return default
    
    @staticmethod
    def dump(filepath: Path, data: Dict[str, Any]) -> None:
        with open(filepath, "w") as file:
            json.dump(data, file)
    
    def __init__(
        self,
        filepath: str,
        default: Dict[str, Any]={
            "sound_font_path": None
        }
    ) -> bool:
        self.filepath = Path(filepath)
        self.default = default
        
        try:
            self.config = self.load(self.filepath, self.default)
        except:
            self.dump(self.filepath, self.default)
            self.config = self.default
    
    def __str__(self) -> str: return f"{self.__class__.__name__}({self.config})"
    def __repr__(self) -> str: return self.__str__()
    def refresh(self) -> None: self.dump(self.filepath, self.config)
    
    @property
    def sound_font_path(self) -> Optional[str]: return self.config.get("sound_font_path")

# ! Main
class SeaPlayer(App):
    TITLE = f"{__title__} v{__version__}"
    CSS_PATH = "ui.css"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="/", action="minus_rewind", description="Rewind -1 sec"),
        Binding(key="*", action="plus_rewind", description="Rewind +1 sec"),
        Binding(key="-", action="minus_volume", description="Volume -1%"),
        Binding(key="+", action="plus_volume", description="Volume +1%")
    ]
    
    SEA_PLAYER_CONFIG = SeaPlayerConfig(CONFIG_PATH)
    
    currect_sound_uuid: Optional[str] = None
    currect_volume = 1.0
    last_playback_status: Optional[Literal["Stoped", "Playing", "Paused"]] = None
    playback_mode: int = 0
    playback_mode_blocked: bool = False
    
    started: bool = True
    
    def gcs(self) -> Optional[Sound]:
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.music_list.get(self.currect_sound_uuid)) is not None:
                return sound
    
    async def aio_gcs(self):
        if self.currect_sound_uuid is not None:
            if (sound:=await self.music_list_view.music_list.aio_get(self.currect_sound_uuid)) is not None:
                return sound
    
    def get_sound_seek(self) -> Tuple[str, Optional[float], Optional[float]]:
        if (sound:=self.gcs()) is not None:
            pos = sound.get_pos()
            minutes, seconds = round(pos // 60), round(pos % 60)
            return f"{minutes}:{str(seconds).rjust(2,'0')} | {str(round(sound.get_volume()*100)).rjust(3)}%", pos, sound.duration
        return "0:00 |   0%", None, None
    
    def get_sound_selected_label_text(self) -> str:
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.music_list.get(self.currect_sound_uuid)) is not None:
                return f"({check_status(sound)}): {get_sound_basename(sound)}"
            return "<sound not found>"
        return "<sound not selected>"
    
    async def aio_get_sound_selected_label_text(self) -> str:
        if self.currect_sound_uuid is not None:
            if (sound:=await self.music_list_view.music_list.aio_get(self.currect_sound_uuid)) is not None:
                return f"({check_status(sound)}): {get_sound_basename(sound)}"
            return "<sound not found>"
        return "<sound not selected>"
    
    def gpms(self, modes: Tuple[str, str, str]=("(PLAY)", "(REPLAY SOUND)", "(REPLAY LIST)")) -> str: return modes[self.playback_mode]
    def switch_playback_mode(self) -> None:
        if self.playback_mode == 2: self.playback_mode = 0
        else: self.playback_mode += 1
    
    async def update_selected_label_text(self) -> None:
        while self.started:
            if (sound:=await self.aio_gcs()) is not None:
                status = check_status(sound)
                if (self.last_playback_status is not None) and (self.last_playback_status != status):
                    self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
                
                if (status == "Stoped") and (self.last_playback_status == "Playing"):
                    if self.playback_mode == 1: sound.play()
                    elif self.playback_mode == 2:
                        if (sound:=await self.set_sound_for_playback(sound_uuid:=self.music_list_view.get_next_sound_uuid(self.currect_sound_uuid), True)) is not None:
                            self.playback_mode_blocked = True
                            self.music_list_view.select_list_item_from_sound_uuid(sound_uuid)
                            sound.play()
                
                self.last_playback_status = status
            await asyncio.sleep(0.5)
    
    def compose(self) -> ComposeResult:
        # * Play Screen
        self.music_play_screen = Static(classes="screen-box")
        self.music_play_screen.border_title = "Player"
        
        self.music_selected_label = Label(self.get_sound_selected_label_text(), classes="music-selected-label")
        self.music_image = ImageLabel()
        
        # * Compositions Screen
        self.music_list_screen = Static(classes="screen-box")
        self.music_list_screen.border_title = "Music List"
        
        self.music_list_view = MusicListView(classes="music-list-view")
        self.music_list_add_input = Input(placeholder="Media filepath", classes="music-list-screen-add-input")
        
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
                        yield Button("Play/Stop", id="button-play-stop", classes="button-sound-control")
                        yield Static(classes="pass-one-width")
                        yield Button("Pause/Unpause", id="button-pause-unpause", classes="button-sound-control")
                        yield Static(classes="pass-one-width")
                        yield Button(self.gpms(), id="switch-playback-mode", classes="button-sound-control")
        with self.music_list_screen:
            yield self.music_list_view
            with Horizontal(classes="music-list-screen-add-box"):
                yield self.music_list_add_input
                yield Button("+", id="plus-sound", classes="music-list-screen-add-button")
        yield Footer()
        
        self.run_worker(self.update_selected_label_text, name="UPDATE_SELECTED_LABEL")
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "plus-sound":
            path = self.music_list_add_input.value
            self.music_list_add_input.value = ""
            
            if path.replace(" ", "") != "":
                try:
                    if await aio_is_midi_file(path):
                        if self.SEA_PLAYER_CONFIG.sound_font_path is not None:
                            sfp = self.SEA_PLAYER_CONFIG.sound_font_path
                        else:
                            sfp = SOUND_FONTS_PATH
                        sound = Sound.from_midi(path, path_sound_fonts=sfp)
                    else: sound = Sound(path)
                except: sound = None
                if sound is not None: await self.music_list_view.aio_add_sound(sound)
        
        elif (event.button.id == "button-play-stop") or (event.button.id == "button-pause-unpause"):
            if (sound:=await self.aio_gcs()) is not None:
                
                if event.button.id == "button-play-stop":
                    if sound.playing:
                        self.last_playback_status = "Stoped"
                        sound.stop()
                    else:
                        self.last_playback_status = "Playing"
                        sound.play()
                elif event.button.id == "button-pause-unpause":
                    if sound.playing:
                        if sound.paused:
                            self.last_playback_status = "Playing"
                            sound.unpause()
                        else:
                            self.last_playback_status = "Paused"
                            sound.pause()
                
                self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
        elif event.button.id == "switch-playback-mode":
            self.switch_playback_mode()
            event.button.label = self.gpms()
    
    async def set_sound_for_playback(self, sound_uuid: Optional[str], playback_mode_blocked: Optional[bool]=None) -> Optional[Sound]:
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
                self.music_image.update_image(image_from_bytes(sound.icon_data))
            self.music_selected_label.update(await self.aio_get_sound_selected_label_text())
            return sound
    
    async def on_list_view_selected(self, selected: MusicListView.Selected):
        await self.set_sound_for_playback(getattr(selected.item, "sound_uuid", None))
    
    async def action_plus_rewind(self):
        if (sound:=await self.aio_gcs()) is not None:
            sound.set_pos(sound.get_pos()+1)
    
    async def action_minus_rewind(self):
        if (sound:=await self.aio_gcs()) is not None:
            sound.set_pos(sound.get_pos()-1)
    
    async def action_plus_volume(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if (vol:=round(sound.get_volume()+0.01, 2)) <= 2:
                self.currect_volume = vol
                sound.set_volume(vol)
    
    async def action_minus_volume(self) -> None:
        if (sound:=await self.aio_gcs()) is not None:
            if (vol:=round(sound.get_volume()-0.01, 2)) >= 0:
                self.currect_volume = vol
                sound.set_volume(vol)
    
    async def action_quit(self):
        self.started = False
        if (sound:=await self.aio_gcs()) is not None:
            sound.stop()
        return await super().action_quit()

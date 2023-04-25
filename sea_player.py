import os
import sys
import json
import uuid
from io import BytesIO
from pathlib import Path
# > Sound Works
from playsoundsimple import Sound
from playsoundsimple.Units import SOUND_FONTS_PATH
# > Image Works
from PIL import Image
from tpng import TPNG
# > Graphics
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label, ListItem, ListView, Input, Button
from textual.binding import Binding
from rich.progress import Progress, BarColumn, TextColumn
# > Typing
from typing import Optional, Literal, Dict, Tuple, Any

# ! Metadata
__title__ = "SeaPlayer"
__version__ = "0.2.3"
__author__ = "Romanin"
__email__ = "semina054@gmail.com"

# ! Contains
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'): LOCALDIR = os.path.dirname(sys.executable)
else: LOCALDIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(LOCALDIR, "config.json")

# ! Functions
def check_status(sound: Sound) -> Literal["Stoped", "Playing", "Paused"]:
    if sound.playing:
        if sound.paused: return "Paused"
        else: return "Playing"
    return "Stoped"

def _get_status() -> Tuple[str, Optional[float], Optional[float]]: return "", None, None

def image_from_bytes(data: Optional[bytes]) -> Optional[Image.Image]:
    if data is not None: return Image.open(BytesIO(data))

def get_sound_basename(sound: Sound) -> str:
    if sound.title is not None:
        if sound.artist is not None:
            return f"{sound.artist} - {sound.title}"
        return f"{sound.title}"
    return f"{os.path.basename(sound.name)}"

def is_midi_file(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        return file.read(4) == b"MThd"

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

# ! Classes
class MusicList:
    def __init__(self, **child_sounds: Sound) -> None:
        self.sounds: Dict[str, Sound] = {}
        for key in child_sounds:
            if isinstance(child_sounds[key], Sound):
                self.sounds[key] = child_sounds[key]
    
    def exists(self, sound_uuid: str) -> bool:
        return sound_uuid in self.sounds.keys()
    
    def add(self, sound: Sound) -> str:
        sound_uuid = str(uuid.uuid4())
        self.sounds[sound_uuid] = sound
        return sound_uuid
    
    def get(self, sound_uuid: str) -> Optional[Sound]:
        return self.sounds.get(sound_uuid)

# ! Types
class MusicListViewItem(ListItem):
    def __init__(
        self,
        title: str="",
        first_subtitle: str="",
        second_subtitle: str="",
        sound_uuid: Optional[str]=None
    ) -> None:
        super().__init__(classes="music-list-view-item")
        self.title_label = Label(title, classes="music-list-view-item-title-label")
        self.first_subtitle_label = Label(f" {first_subtitle}", classes="music-list-view-item-subtitle-label")
        self.second_subtitle_label = Label(f" {second_subtitle}", classes="music-list-view-item-subtitle-label")
        self.sound_uuid = sound_uuid
        
        self.compose_add_child(self.title_label)
        self.compose_add_child(self.first_subtitle_label)
        self.compose_add_child(self.second_subtitle_label)
    
    def update_labels(
        self,
        title: Optional[str]=None,
        first_subtitle: Optional[str]=None,
        second_subtitle: Optional[str]=None,
    ) -> None:
        if title is not None: self.title_label.update(title)
        if first_subtitle is not None: self.first_subtitle_label.update(title)
        if second_subtitle is not None: self.second_subtitle_label.update(title)

class MusicListView(ListView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.music_list: MusicList = MusicList(classes="music-list-view")
    
    def add_sound(self, sound: Sound) -> str:
        sound_uuid = self.music_list.add(sound)
        self.append(
            MusicListViewItem(
                f"{get_sound_basename(sound)}",
                "{duration} sec, {channel_mode}, {samplerate} Hz, {bitrate} kbps".format(
                    duration=round(sound.duration),
                    channel_mode="Mono" if sound.channels <= 1 else "Stereo",
                    samplerate=round(sound.samplerate),
                    bitrate=round(sound.bitrate / 1000)
                ),
                os.path.abspath(sound.name),
                sound_uuid
            )
        )
        return sound_uuid
    
    def get_sound(self, sound_uuid: str) -> Optional[Sound]:
        return self.music_list.get(sound_uuid)

class IndeterminateProgress(Static):
    def __init__(self, getfunc=_get_status, fps: int=30):
        super().__init__("", classes="indeterminate-progress-bar")
        self._bar = Progress(BarColumn(), TextColumn("{task.description}"))
        self._task_id = self._bar.add_task("", total=None)
        self._fps = fps
        self._getfunc = getfunc
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/30, self.update_progress_bar)
    
    def upgrade_task(self, description: str="", completed: Optional[float]=None, total: Optional[float]=None) -> None:
        self._bar.update(self._task_id, total=total, completed=completed, description=description)
    
    def update_progress_bar(self) -> None:
        d, c, t = self._getfunc()
        if self._bar.columns[0].bar_width != (self.size[0]-len(d)-1):
            self._bar.columns[0].bar_width = self.size[0]-len(d)-1
        self.upgrade_task(completed=c, total=t, description=d)
        self.update(self._bar)

class ImageLabel(Label):
    def __init__(self, image: Optional[Image.Image]=None):
        super().__init__("<image not found>", classes="image-label")
        self.image = image
        self.tpng_image = TPNG(self.image) if self.image is not None else None
        self.last_image_size = None
        self.image_text = "<image not found>"
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/2, self.update_image_label)
    
    def update_image_label(self):
        if self.tpng_image is not None:
            new_size = (self.size[0]-4, self.size[1])
            if self.last_image_size != new_size:
                self.tpng_image.reset()
                self.tpng_image.resize(new_size)
                self.image_text = self.tpng_image.to_rich_image()
        else:
            self.image_text = "<image not found>"
        
        self.update(self.image_text)
    
    def update_image(self, image: Optional[Image.Image]=None) -> None:
        self.image = image
        self.tpng_image = TPNG(self.image) if self.image is not None else None
        if self.tpng_image is not None:
            self.tpng_image.reset()
            self.tpng_image.resize((self.size[0]-4, self.size[1]))
            self.image_text = self.tpng_image.to_rich_image()
        else:
            self.image_text = "<image not found>"

# ! Main
class SeaPlayer(App):
    TITLE = f"{__title__} v{__version__}"
    CSS_PATH = "ui.css"
    BINDINGS = [
        Binding(key="/", action="minus_rewind", description="Rewind -1 sec"),
        Binding(key="*", action="plus_rewind", description="Rewind +1 sec"),
        Binding(key="-", action="minus_volume", description="Volume -1%"),
        Binding(key="+", action="plus_volume", description="Volume +1%")
    ]
    
    SEA_PLAYER_CONFIG = SeaPlayerConfig(CONFIG_PATH)
    
    currect_sound_uuid: Optional[str] = None
    currect_volume = 1.0
    
    def get_sound_seek(self) -> Tuple[str, Optional[float], Optional[float]]:
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.music_list.get(self.currect_sound_uuid)) is not None:
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
        with self.music_list_screen:
            yield self.music_list_view
            with Horizontal(classes="music-list-screen-add-box"):
                yield self.music_list_add_input
                yield Button("+", id="plus-sound", classes="music-list-screen-add-button")
        yield Footer()
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "plus-sound":
            path = self.music_list_add_input.value
            self.music_list_add_input.value = ""
            if path.replace(" ", "") != "":
                try:
                    if is_midi_file(path):
                        if self.SEA_PLAYER_CONFIG.sound_font_path is not None: sfp = self.SEA_PLAYER_CONFIG.sound_font_path
                        else: sfp = SOUND_FONTS_PATH
                        sound = Sound.from_midi(path, path_sound_fonts=sfp)
                    else: sound = Sound(path)
                except: sound = None
                if sound is not None: self.music_list_view.add_sound(sound)
        elif (event.button.id == "button-play-stop") or (event.button.id == "button-pause-unpause"):
            if self.currect_sound_uuid is not None:
                if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                    if event.button.id == "button-play-stop":
                        if sound.playing: sound.stop()
                        else: sound.play()
                    elif event.button.id == "button-pause-unpause":
                        if sound.playing:
                            if sound.paused: sound.unpause()
                            else: sound.pause()
                    self.music_selected_label.update(self.get_sound_selected_label_text())
    
    def on_list_view_selected(self, selected: MusicListView.Selected):
        sound_uuid = getattr(selected.item, "sound_uuid", None)
        if sound_uuid is not None:
            if self.currect_sound_uuid is not None:
                if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                    sound.stop()
            self.currect_sound_uuid = sound_uuid
            if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                sound.set_volume(self.currect_volume)
                self.music_image.update_image(image_from_bytes(sound.icon_data))
            self.music_selected_label.update(self.get_sound_selected_label_text())
    
    def action_plus_rewind(self):
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                sound.set_pos(sound.get_pos()+1)
    
    def action_minus_rewind(self):
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                sound.set_pos(sound.get_pos()-1)
    
    def action_plus_volume(self) -> None:
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                if (vol:=round(sound.get_volume()+0.01, 2)) <= 2:
                    self.currect_volume = vol
                    sound.set_volume(vol)
    
    def action_minus_volume(self) -> None:
        if self.currect_sound_uuid is not None:
            if (sound:=self.music_list_view.get_sound(self.currect_sound_uuid)) is not None:
                if (vol:=round(sound.get_volume()-0.01, 2)) >= 0:
                    self.currect_volume = vol
                    sound.set_volume(vol)

# ! Start
if __name__ == "__main__":
    app = SeaPlayer()
    app.run()
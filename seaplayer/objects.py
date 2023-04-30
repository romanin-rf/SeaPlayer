from PIL import Image
from tpng import TPNG
from playsoundsimple import Sound
from textual.widgets import Static, Label, ListItem, ListView
from rich.progress import Progress, BarColumn, TextColumn
# > Typing
from typing import Optional
# > Local Import's
from .functions import *
from .types import *

# ! Objects
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
    
    def get_sound(self, sound_uuid: str) -> Optional[Sound]: return self.music_list.get(sound_uuid)
    
    async def aio_add_sound(self, sound: Sound):
        sound_uuid = await self.music_list.aio_add(sound)
        await self.append(
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
    
    def get_items_count(self) -> int: return len(self.children)
    def exists_item_index(self, index: int) -> bool: return 0 >= index < self.get_items_count()
    def get_item_index_from_sound_uuid(self, sound_uuid: str) -> Optional[int]:
        item: MusicListViewItem
        for idx, item in enumerate(self.children):
            if item.sound_uuid == sound_uuid:
                return idx
    def get_item_from_index(self, index: int) -> Optional[MusicListViewItem]:
        try: return self.children[index]
        except:
            try: return self.children[0]
            except: pass
    def get_next_sound_uuid(self, sound_uuid: str) -> Optional[str]:
        if (index:=self.get_item_index_from_sound_uuid(sound_uuid)) is not None:
            if (mli:=self.get_item_from_index(index+1)) is not None:
                return mli.sound_uuid
    
    def select_list_item_from_index(self, index: Optional[int]) -> None:
        try: self.post_message(self.Highlighted(self, self.children[index]))
        except: pass
    
    def select_list_item_from_sound_uuid(self, sound_uuid: str) -> None:
        try:
            super().on_list_item__child_clicked(
                ListItem._ChildClicked(
                    self.children[self.get_item_index_from_sound_uuid(sound_uuid)]
                )
            )
        except: pass


class IndeterminateProgress(Static):
    def __init__(self, getfunc=get_bar_status, fps: int=15):
        super().__init__("", classes="indeterminate-progress-bar")
        self._bar = Progress(BarColumn(), TextColumn("{task.description}"))
        self._task_id = self._bar.add_task("", total=None)
        self._fps = fps
        self._getfunc = getfunc
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/self._fps, self.update_progress_bar)
    
    def upgrade_task(self, description: str="", completed: Optional[float]=None, total: Optional[float]=None) -> None:
        self._bar.update(self._task_id, total=total, completed=completed, description=description)
    
    def update_progress_bar(self) -> None:
        d, c, t = self._getfunc()
        if self._bar.columns[0].bar_width != (self.size[0]-len(d)-1):
            self._bar.columns[0].bar_width = self.size[0]-len(d)-1
        self.upgrade_task(completed=c, total=t, description=d)
        self.update(self._bar)


class ImageLabel(Label):
    def __init__(self, image: Optional[Image.Image]=None, fps: int=2):
        super().__init__("<image not found>", classes="image-label")
        self.image: Optional[Image.Image] = image
        self.tpng_image: Optional[TPNG] = TPNG(self.image) if self.image is not None else None
        self.last_image_size: Optional[Tuple[int, int]] = None
        self.image_text = "<image not found>"
        self._fps = fps
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/self._fps, self.update_image_label)
    
    def update_image_label(self):
        if self.tpng_image is not None:
            new_size = (self.size[0]-4, self.size[1])
            if self.last_image_size != new_size:
                self.tpng_image.reset()
                self.tpng_image.resize(new_size)
                self.image_text = self.tpng_image.to_rich_image()
                self.last_image_size = new_size
        else:
            self.image_text = "<image not found>"
        
        self.update(self.image_text)
    
    def update_image(self, image: Optional[Image.Image]=None) -> None:
        self.image = image
        self.tpng_image = TPNG(self.image) if (self.image is not None) else None
        
        if self.tpng_image is not None:
            self.tpng_image.reset()
            self.tpng_image.resize((self.size[0]-4, self.size[1]))
            self.image_text = self.tpng_image.to_rich_image()

from textual.widgets import Label, ListItem, ListView
# > Typing
from typing import Optional
# > Local Import's
from .Labels import FillLabel
from ..types import MusicList
from ..codeсbase import CodecBase
from ..functions import get_sound_basename, aiter

# ! Children Classes
class MusicListViewItem(ListItem):
    DEFAULT_CSS = """
    MusicListViewItem {
        height: 4;
    }
    MusicListViewItem .title-label {
        height: 1;
        color: #cacaca;
    }
    MusicListViewItem .subtitle-label {
        height: 1;
        color: #a9a9a9;
    }
    """
    
    def __init__(
        self,
        title: str="",
        first_subtitle: str="",
        second_subtitle: str="",
        sound_uuid: Optional[str]=None
    ) -> None:
        super().__init__()
        self.title_label = Label(title, classes="title-label")
        self.first_subtitle_label = Label(f" {first_subtitle}", classes="subtitle-label")
        self.second_subtitle_label = Label(f" {second_subtitle}", classes="subtitle-label")
        self.sound_uuid = sound_uuid
        
        self.compose_add_child(self.title_label)
        self.compose_add_child(self.first_subtitle_label)
        self.compose_add_child(self.second_subtitle_label)
        self.compose_add_child(FillLabel())
    
    async def update_labels(
        self,
        title: Optional[str]=None,
        first_subtitle: Optional[str]=None,
        second_subtitle: Optional[str]=None,
    ) -> None:
        if title is not None: self.title_label.update(title)
        if first_subtitle is not None: self.first_subtitle_label.update(title)
        if second_subtitle is not None: self.second_subtitle_label.update(title)

# ! Main Class
class MusicListView(ListView):
    DEFAULT_CSS = """
    MusicListView {
        height: 1fr;
    }
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.music_list: MusicList = MusicList()
    
    def add_sound(self, sound: CodecBase) -> str:
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
                sound.name,
                sound_uuid
            )
        )
        return sound_uuid
    
    def get_sound(self, sound_uuid: str) -> Optional[CodecBase]:
        return self.music_list.get(sound_uuid)
    
    async def aio_get_sound(self, sound_uuid: str) -> Optional[CodecBase]:
        return self.music_list.get(sound_uuid)
    
    async def aio_add_sound(self, sound: CodecBase):
        sound_uuid = await self.music_list.aio_add(sound)
        await self.append(
            MusicListViewItem(
                f"{get_sound_basename(sound)}",
                "{duration} sec, {channel_mode}, {samplerate} Hz, {bitrate} kbps, {codec_name}".format(
                    duration=round(sound.duration),
                    channel_mode="Mono" if sound.channels <= 1 else "Stereo",
                    samplerate=round(sound.samplerate),
                    bitrate=round(sound.bitrate / 1000),
                    codec_name=sound.codec_name
                ),
                sound.name,
                sound_uuid
            )
        )
        return sound_uuid
    
    def get_items_count(self) -> int:
        return len(self.children)
    
    def exists_item_index(self, index: int) -> bool:
        return 0 >= index < self.get_items_count()
    
    def get_item_index_from_sound_uuid(self, sound_uuid: str) -> Optional[int]:
        item: MusicListViewItem
        for idx, item in enumerate(self.children):
            if item.sound_uuid == sound_uuid:
                return idx
    
    def get_item_from_index(self, index: int) -> Optional[MusicListViewItem]:
        try:
            return self.children[index]
        except:
            try:
                return self.children[0]
            except:
                pass
    
    def get_next_sound_uuid(self, sound_uuid: str) -> Optional[str]:
        if (index:=self.get_item_index_from_sound_uuid(sound_uuid)) is not None:
            if (mli:=self.get_item_from_index(index+1)) is not None:
                return mli.sound_uuid
    
    def select_list_item_from_sound_uuid(self, sound_uuid: str) -> None:
        try:
            super()._on_list_item__child_clicked(
                ListItem._ChildClicked(
                    self.children[self.get_item_index_from_sound_uuid(sound_uuid)]
                )
            )
        except: pass
    
    async def aio_get_item_from_index(self, index: int) -> Optional[MusicListViewItem]:
        try: return self.children[index]
        except:
            try: return self.children[0]
            except: pass
    
    async def aio_get_item_index_from_sound_uuid(self, sound_uuid: str) -> Optional[int]:
        item: MusicListViewItem
        async for idx, item in aiter(enumerate(self.children)):
            if item.sound_uuid == sound_uuid:
                return idx
    
    async def aio_get_next_sound_uuid(self, sound_uuid: str) -> Optional[str]:
        if (index:=await self.aio_get_item_index_from_sound_uuid(sound_uuid)) is not None:
            if (mli:=await self.aio_get_item_from_index(index+1)) is not None:
                return mli.sound_uuid
    
    async def aio_select_list_item_from_sound_uuid(self, sound_uuid: str) -> None:
        try:
            super()._on_list_item__child_clicked(
                ListItem._ChildClicked(
                    self.children[await self.aio_get_item_index_from_sound_uuid(sound_uuid)]
                )
            )
        except:
            pass
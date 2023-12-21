import asyncio
from vkpymusic import Service
from seaplayer.codecs.URLS import URLSoundCodec
from seaplayer.codecs.AnySound import AnySound
# > Typing
from typing import Optional, Tuple
# > Local Imports
from .units import PATCHER, VKM_MAIN_PATTERN

# ! Methods
def parse_vkm(url: str) -> Tuple[int, int]:
    d = PATCHER.check(VKM_MAIN_PATTERN, url)
    if not isinstance(d, dict):
        raise RuntimeError("The values from the 'url' could not be parsed.")
    return d.get("uid"), d.get("sid")

# ! Main Class
class VKMCodec(URLSoundCodec):
    codec_name = "VKM"
    codec_priority = 5.999
    
    # ! Check Methods
    @staticmethod
    def is_this_codec(url: str) -> bool:
        return isinstance(PATCHER.check(VKM_MAIN_PATTERN, url), dict)
    
    @staticmethod
    async def aio_is_this_codec(url: str) -> bool:
        return isinstance(PATCHER.check(VKM_MAIN_PATTERN, url), dict)
    
    # ! Main Functions
    def __init__(
        self,
        url: str,
        sound_device_id: Optional[int]=None,
        vkm_service: Optional[Service]=None,
        aio_init: bool=False,
        **kwargs
    ) -> None:
        if vkm_service is None:
            raise RuntimeError("The 'service' argument is None.")
        uid, sid = parse_vkm(url)
        self.song = vkm_service.get_songs_by_userid(uid, 1, sid)[0]
        self._title = (self.song.title if (len(self.song.title) > 0) else None) if isinstance(self.song.title, str) else None
        self._artist = (self.song.artist if (len(self.song.artist) > 0) else None) if isinstance(self.song.artist, str) else None
        super().__init__(self.song.url, sound_device_id, aio_init, **kwargs)
        self.name = url
    
    @staticmethod
    async def __aio_init__(
        url: str,
        sound_device_id: Optional[int]=None,
        vkm_service: Optional[Service]=None,
        **kwargs
    ):
        self = VKMCodec(url, sound_device_id, vkm_service, aio_init=True)
        self._sound = await asyncio.to_thread(AnySound.from_url, self.song.url, device_id=sound_device_id)
        return self
    
    # ! Properys
    @property
    def title(self) -> str:
        return self._title
    
    @property
    def artist(self) -> str:
        return self._artist
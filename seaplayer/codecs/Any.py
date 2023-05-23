import os
import hashlib
import aiofiles
# > Sound Works
from playsoundsimple import Sound
# > Typing
from typing import Optional
# > Local Imports
from ..codeсbase import CodecBase


class AnyCodec(CodecBase):
    codec_name: str = "Any"
    
    # ! Initialized
    def __init__(self, path: str, **kwargs) -> None:
        self.name = os.path.abspath(path)
        self._sound = Sound(self.name)
    
    def __sha1__(self, buffer_size: int) -> str:
        sha1 = hashlib.sha1()
        with open(self.name, "rb") as file:
            while True:
                data = file.read(buffer_size)
                if not data: break
                sha1.update(data)
        return sha1.hexdigest()
    
    async def __aio_sha1__(self, buffer_size: int) -> str:
        sha1 = hashlib.sha1()
        async with aiofiles.open(self.name, "rb") as file:
            while True:
                data = await file.read(buffer_size)
                if not data: break
                sha1.update(data)
        return sha1.hexdigest()
    
    # ! Info
    @property
    def duration(self) -> float: return self._sound.duration
    @property
    def channels(self) -> int: return self._sound.channels
    @property
    def samplerate(self) -> int: return self._sound.samplerate
    @property
    def bitrate(self) -> int: return self._sound.bitrate
    
    # ! Playback Info
    @property
    def playing(self) -> bool: return self._sound.playing
    @property
    def paused(self) -> bool: return self._sound.paused
    
    # ! Sound Info
    @property
    def title(self) -> Optional[str]: return self._sound.title
    @property
    def artist(self) -> Optional[str]: return self._sound.artist
    @property
    def album(self) -> Optional[str]: return self._sound.album
    @property
    def icon_data(self) -> Optional[bytes]: return self._sound.icon_data
    
    # ! Functions
    def play(self) -> None: self._sound.play()
    def stop(self) -> None: self._sound.stop()
    def pause(self) -> None: self._sound.pause()
    def unpause(self) -> None: self._sound.unpause()
    def get_volume(self) -> float: return self._sound.get_volume()
    def set_volume(self, value: float) -> None: self._sound.set_volume(value)
    def get_pos(self) -> float: return self._sound.get_pos()
    def set_pos(self, value: float) -> None: self._sound.set_pos(value)
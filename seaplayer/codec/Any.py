import os
import hashlib
import asyncio
import aiofiles
# > Sound Works
from ..modules.sound import Sound, DATA
# > Typing
from typing import Optional, Callable, NoReturn
# > Local Imports
from ..codecbase import CodecBase


class AnyCodec(CodecBase):
    codec_name: str = "Any"
    
    # ! Initialized
    def __init__(self, path: str, sender: Callable[[DATA], None], **kwargs) -> None:
        self.name = os.path.abspath(path)
        self._sound = Sound(self.name, **kwargs)
        self.__playing: bool = False
        self.__paused: bool = False
        self.__volume: float = 1.0
        self.sender = sender
    
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
    def playing(self) -> bool: return self.__playing
    @property
    def paused(self) -> bool: return self.__paused
    
    # ! Sound Info
    @property
    def title(self) -> Optional[str]: return self._sound.title
    @property
    def artist(self) -> Optional[str]: return self._sound.artist
    @property
    def album(self) -> Optional[str]: return self._sound.album
    @property
    def icon_data(self) -> Optional[bytes]: return self._sound.icon_data
    
    # ! Private Functions
    async def check_pause(self) -> None:
        while self.__paused: await asyncio.sleep(0)
    
    async def loop(self) -> None:
        async for data in self._sound:
            if not self.__playing:
                break
            await self.check_pause()
            await self.sender(data * self.__volume)
    
    # ! Functions
    async def play(self) -> NoReturn:
        self.__playing = True
        await self.loop()
    
    def stop(self) -> None:
        self.__playing = False
        self._sound.stop()
    def pause(self) -> None:
        self.__paused = True
    def unpause(self) -> None: self.__paused = False
    def get_volume(self) -> float: return self.__volume
    def set_volume(self, value: float) -> None: self.__volume = value
    def get_pos(self) -> float: return self._sound.get_pos()
    def set_pos(self, value: float) -> None: self._sound.set_pos(value)
import os
import aiofiles
# > Typing Import
from typing import Callable
# > Local Imports
from .Any import AnyCodec
from ..modules.sound import Sound, DATA

# ! Codec
class MIDICodec(AnyCodec):
    codec_name: str = "MIDI"
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, 'rb') as file:
            return file.read(4) == b"MThd"
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, 'rb') as file:
            return await file.read(4) == b"MThd"
    
    # ! Initialized
    def __init__(
        self,
        path: str,
        sender: Callable[[DATA], None],
        aio_init: bool = False,
        **kwargs
    ) -> None:
        self.name = os.path.abspath(path)
        if not aio_init: self._sound = Sound.from_midi(self.name, **kwargs)
        self.sender = sender
        self.__playing: bool = False
        self.__paused: bool = False
        self.__volume: float = 1.0
    
    @staticmethod
    async def __aio_init__(
        path: str,
        sender: Callable[[DATA], None],
        **kwargs
    ):
        self = MIDICodec(path, sender, aio_init=True, **kwargs)
        self.name = os.path.abspath(path)
        self._sound = await Sound.aio_from_midi(self.name, **kwargs)
        self.__playing: bool = False
        self.__paused: bool = False
        self.__volume: float = 1.0
        self.sender = sender
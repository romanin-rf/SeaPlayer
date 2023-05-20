import os
import asyncio
import aiofiles
from asyncio import AbstractEventLoop
from tempfile import mkstemp
# > Sound Works
from playsoundsimple import Sound
from playsoundsimple.units import SOUND_FONTS_PATH, FLUID_SYNTH_PATH
from playsoundsimple.exceptions import FileTypeError
from playsoundsimple.player import SoundFP, get_sound_filepath
# > Local Imports
from .MP3 import MP3Codec


# ! Codec Types
class MIDISound(Sound):
    async def aio_from_midi(
        fp: SoundFP,
        sound_fonts_path: str=SOUND_FONTS_PATH,
        **kwargs
    ):
        path, is_temp = get_sound_filepath(fp, filetype=".midi")
        if path is None: raise FileTypeError(fp)
        npath = mkstemp(suffix=".wav")[1]
        
        process = await asyncio.create_subprocess_exec(FLUID_SYNTH_PATH, "-ni", sound_fonts_path, path, "-F", npath, "-q")
        await process.wait()
        
        if is_temp:
            try: os.remove(path)
            except: pass
        
        return Sound(npath, **{"is_temp": True, **kwargs})

# ! Codec
class MIDICodec(MP3Codec):
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
    def __init__(self, path: str, aio_init: bool=False, **kwargs) -> None:
        self.name = os.path.abspath(path)
        if not aio_init:
            self._sound = Sound.from_midi(self.name, **kwargs)
    
    @staticmethod
    async def __aio_init__(path: str, **kwargs):
        self = MIDICodec(path, aio_init=True)
        self._sound = await MIDISound.aio_from_midi(self.name, **kwargs)
        return self
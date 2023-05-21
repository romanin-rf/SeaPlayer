import os
import asyncio
import aiofiles
import subprocess
from tempfile import mkstemp
# > Sound Works
from playsoundsimple import Sound
from playsoundsimple.units import SOUND_FONTS_PATH, FLUID_SYNTH_PATH
from playsoundsimple.exceptions import FileTypeError
from playsoundsimple.player import SoundFP, get_sound_filepath
# > Typing Import
from typing import Optional
# > Local Imports
from .Any import AnyCodec


# ! Codec Types
class MIDISound(Sound):
    async def aio_from_midi(
        fp: SoundFP,
        sound_fonts_path: Optional[str]=None,
        **kwargs
    ):
        path, is_temp = get_sound_filepath(fp, filetype=".midi")
        sound_fonts_path = sound_fonts_path or SOUND_FONTS_PATH
        if path is None: raise FileTypeError(fp)
        npath = mkstemp(suffix=".wav")[1]
        
        process = await asyncio.create_subprocess_exec(
            FLUID_SYNTH_PATH, "-ni", sound_fonts_path, path, "-F", npath, "-q",
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await process.wait()
        
        if is_temp:
            try: os.remove(path)
            except: pass
        
        return Sound(npath, **{"is_temp": True, **kwargs})
    
    def from_midi(
        fp: SoundFP,
        sound_fonts_path: Optional[str]=None,
        **kwargs
    ):
        path, is_temp = get_sound_filepath(fp, filetype=".midi")
        sound_fonts_path = sound_fonts_path or SOUND_FONTS_PATH
        if path is None: raise FileTypeError(fp)
        npath = mkstemp(suffix=".wav")[1]
        
        subprocess.call(
            [FLUID_SYNTH_PATH, "-ni", sound_fonts_path, path, "-F", npath, "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        if is_temp:
            try: os.remove(path)
            except: pass
        
        return Sound(npath, **{"is_temp": True, **kwargs})

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
    def __init__(self, path: str, aio_init: bool=False, **kwargs) -> None:
        self.name = os.path.abspath(path)
        if not aio_init:
            self._sound = MIDISound.from_midi(self.name, **kwargs)
    
    @staticmethod
    async def __aio_init__(path: str, **kwargs):
        self = MIDICodec(path, aio_init=True)
        self._sound = await MIDISound.aio_from_midi(self.name, **kwargs)
        return self
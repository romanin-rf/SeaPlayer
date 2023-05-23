import os
import asyncio
import subprocess
import numpy as np
from tempfile import mkstemp
# > Sound Works
import soundfile as sf
from mutagen import File, FileType
from playsoundsimple.units import SOUND_FONTS_PATH, FLUID_SYNTH_PATH
# > Typing
from typing import \
    Optional, Dict, Literal, Generator, Any, Union, AsyncGenerator

# ! Types
DATA = np.ndarray[Any, Union[np.float64, np.float32, np.int32, np.int16]]

# ! Functions
def get_icon_data(file: Optional[FileType]) -> Optional[bytes]:
    if file is not None:
        try: return file["APIC:"].data
        except:
            try: return file["APIC"].data
            except: pass

# ! Sound Class
class Sound:
    def __init__(
        self,
        filepath: str,
        dtype: Literal["float64", "float32", "int32", "int16"]="float32",
        is_temp: bool=False,
        **kwargs
    ) -> None:
        self.name: str = os.path.abspath(filepath)
        self.sound: sf.SoundFile = sf.SoundFile(self.name)
        self.dtype: Literal["float64", "float32", "int32", "int16"] = dtype
        self.is_temp: bool = is_temp
        
        # * Mutagen Info Getting
        mutagen_file = File(self.name)
        
        # * Playback Info
        self.channels: int = self.sound.channels
        self.samplerate: int = self.sound.samplerate
        self.frames: int = self.sound.frames
        self.duration: float = self.sound.frames / self.samplerate
        self.bitrate: int = int(mutagen_file.info.bitrate)
        self.bit_depth: int = round(self.bitrate / (self.samplerate * self.channels))
        
        # * Metadata
        meta_data: Dict[str, str] = self.sound.copy_metadata()
        
        self.icon_data: Optional[bytes] = get_icon_data(mutagen_file)
        self.title: Optional[str] = meta_data.get('title', None)
        self.artist: Optional[str] = meta_data.get('artist', None)
        self.album: Optional[str] = meta_data.get('album', None)
        self.title: Optional[str] = meta_data.get('title', None)
        self.date: Optional[str] = meta_data.get('date', None)
        
        # * Updateable Vars
        self.currect_frame: int = 0.0
    
    def from_midi(
        filepath: str,
        sound_fonts_path: Optional[str]=None,
        dtype: Literal["float64", "float32", "int32", "int16"]="float32",
        **kwargs
    ):
        sound_fonts_path = sound_fonts_path or SOUND_FONTS_PATH
        new_path = mkstemp(suffix=".wav")[1]
        
        subprocess.call(
            [FLUID_SYNTH_PATH, "-ni", sound_fonts_path, filepath, "-F", new_path, "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        
        return Sound(new_path, **{"is_temp": True, "dtype": dtype, **kwargs})
    
    async def aio_from_midi(
        filepath: str,
        sound_fonts_path: Optional[str]=None,
        dtype: Literal["float64", "float32", "int32", "int16"]="float32",
        **kwargs
    ):
        sound_fonts_path = sound_fonts_path or SOUND_FONTS_PATH
        new_path = mkstemp(suffix=".wav")[1]
        
        process = await asyncio.create_subprocess_exec(
            FLUID_SYNTH_PATH, "-ni", sound_fonts_path, filepath, "-F", new_path, "-q",
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        await process.wait()
        
        return Sound(new_path, **{"is_temp": True, "dtype": dtype, **kwargs})
    
    def __del__(self) -> None:
        self.sound.close()
        try:
            if self.is_temp:
                os.remove(self.name)
        except:
            pass
    
    def __iter__(self) -> Generator[DATA, Any, None]:
        while not self.sound.closed:
            yield self.sound.read(self.samplerate, self.dtype)
            self.currect_frame += self.samplerate
    
    async def __aiter__(self) -> AsyncGenerator[DATA, Any]:
        while not self.sound.closed:
            yield self.sound.read(self.samplerate, self.dtype)
            self.currect_frame += self.samplerate
    
    def set_pos(self, value: float) -> None:
        if 0 >= value <= self.duration:
            self.currect_frame = int(value * self.samplerate)
            self.sound.seek(self.currect_frame)
    
    def get_pos(self) -> float:
        return self.currect_frame / self.samplerate
    
    def stop(self) -> None: self.currect_frame = 0

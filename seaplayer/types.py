import aiofiles
import hashlib
from pathlib import Path
from playsoundsimple import Sound
# > Typing
from typing import Dict, Optional, Tuple, Any
# > Local Imports
from .exceptions import (
    PathNotExistsError,
    NotBooleanError
)

# ! Music List
class MusicList:
    @staticmethod
    def get_file_sha1(path: str, buffer_size: int=65536) -> str:
        sha1 = hashlib.sha1()
        with open(path, "rb") as file:
            while True:
                data = file.read(buffer_size)
                if not data: break
                sha1.update(data)
        return sha1.hexdigest()
    
    @staticmethod
    async def aio_get_file_sha1(path: str, buffer_size: int=65536) -> str:
        sha1 = hashlib.sha1()
        async with aiofiles.open(path, "rb") as file:
            while True:
                data = await file.read(buffer_size)
                if not data: break
                sha1.update(data)
        return sha1.hexdigest()
    
    def __init__(self, **child_sounds: Sound) -> None:
        self.sounds: Dict[str, Sound] = {}
        for key in child_sounds:
            if isinstance(child_sounds[key], Sound):
                self.sounds[key] = child_sounds[key]
    
    def exists(self, sound_uuid: str) -> bool: return sound_uuid in self.sounds.keys()
    def get(self, sound_uuid: str) -> Optional[Sound]: return self.sounds.get(sound_uuid)
    def add(self, sound: Sound) -> str:
        self.sounds[(sound_uuid:=self.get_file_sha1(sound.name))] = sound
        return sound_uuid
    def exists_sha1(self, sound: Sound) -> bool:
        return self.get_file_sha1(sound.name) in self.sounds.keys()
    
    async def aio_exists(self, sound_uuid: str): return sound_uuid in self.sounds.keys()
    async def aio_get(self, sound_uuid: str): return self.sounds.get(sound_uuid)
    async def aio_add(self, sound: Sound):
        self.sounds[(sound_uuid:=await self.aio_get_file_sha1(sound.name))] = sound
        return sound_uuid
    async def aio_exists_sha1(self, sound: Sound) -> bool:
        return await self.aio_get_file_sha1(sound.name) in self.sounds.keys()

class Converter:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
    
    @staticmethod
    def conv(tp: type, value: str) -> Tuple[bool, Optional[Any]]:
        try: return True, tp(value)
        except: return False, None
    
    @staticmethod
    async def aio_conv(tp: type, value: str) -> Tuple[bool, Optional[Any]]:
        try: return True, tp(value)
        except: return False, None
    
    def gen_conv(self, tp: type):
        def conv_wrapper(value: str) -> Tuple[bool, Optional[Any]]:
            return self.conv(tp, value)
        return conv_wrapper
    
    def gen_aio_conv(self, tp: type):
        async def aio_conv_wrapper(value: str) -> Tuple[bool, Optional[Any]]:
            return await self.aio_conv(tp, value)
        return aio_conv_wrapper
    
    # ! Convert Types
    @staticmethod
    def path(value: str) -> str:
        """Checking the existence of a `path`."""
        if not Path(value).exists(): raise PathNotExistsError(value)
        return value
    
    @staticmethod
    def filepath(value: str) -> str:
        """Check if there is a file on the path."""
        path = Path(value)
        if not(path.exists() and path.is_file()): raise PathNotExistsError(value)
        return value
    
    @staticmethod
    def boolean(value: str) -> bool:
        """Converting to `bool`."""
        if value.lower() == "true": return True
        elif value.lower() == "false": return False
        else: raise NotBooleanError(value)
    
    @staticmethod
    def optional(tp: type):
        """This is a type or function decorator for converting a value."""
        def optional_wrapper(value: str):
            if value.lower() != "none":
                return tp(value)
        return optional_wrapper
    
    @staticmethod
    def union(*tps: type):
        def union_wrapper(value: str):
            for tp in tps:
                try: return tp(value)
                except: pass
            raise TypeError(f"Could not convert to any of the listed types: {tps}")
        return union_wrapper
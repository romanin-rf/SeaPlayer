import aiofiles
import hashlib
from playsoundsimple import Sound
# > Typing
from typing import Dict, Optional

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
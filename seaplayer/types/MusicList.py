

# > Typing
from typing import Optional, Dict
# > Local Import's
from ..codeсbase import CodecBase


class MusicList:
    @staticmethod
    def get_file_sha1(sound: CodecBase, buffer_size: int=65536) -> str: return sound.__sha1__(buffer_size)
    
    @staticmethod
    async def aio_get_file_sha1(sound: CodecBase, buffer_size: int=65536) -> str: return await sound.__aio_sha1__(buffer_size)
    
    def __init__(self, **child_sounds: CodecBase) -> None:
        self.sounds: Dict[str, CodecBase] = {}
        for key in child_sounds:
            if isinstance(child_sounds[key], CodecBase):
                self.sounds[key] = child_sounds[key]
    
    def exists(self, sound_uuid: str) -> bool: return sound_uuid in self.sounds.keys()
    def get(self, sound_uuid: str) -> Optional[CodecBase]: return self.sounds.get(sound_uuid)
    def add(self, sound: CodecBase) -> str:
        self.sounds[(sound_uuid:=self.get_file_sha1(sound))] = sound
        return sound_uuid
    def exists_sha1(self, sound: CodecBase) -> bool:
        return self.get_file_sha1(sound) in self.sounds.keys()
    
    async def aio_exists(self, sound_uuid: str): return sound_uuid in self.sounds.keys()
    async def aio_get(self, sound_uuid: str): return self.sounds.get(sound_uuid)
    async def aio_add(self, sound: CodecBase):
        self.sounds[(sound_uuid:=await self.aio_get_file_sha1(sound))] = sound
        return sound_uuid
    async def aio_exists_sha1(self, sound: CodecBase) -> bool:
        return await self.aio_get_file_sha1(sound) in self.sounds.keys()

import uuid
from playsoundsimple import Sound
# > Typing
from typing import Dict, Optional

class MusicList:
    def __init__(self, **child_sounds: Sound) -> None:
        self.sounds: Dict[str, Sound] = {}
        for key in child_sounds:
            if isinstance(child_sounds[key], Sound):
                self.sounds[key] = child_sounds[key]
    
    def exists(self, sound_uuid: str) -> bool: return sound_uuid in self.sounds.keys()
    def add(self, sound: Sound) -> str: self.sounds[(sound_uuid:=str(uuid.uuid4()))] = sound ; return sound_uuid
    def get(self, sound_uuid: str) -> Optional[Sound]: return self.sounds.get(sound_uuid)
    
    async def aio_exists(self, sound_uuid: str): return sound_uuid in self.sounds.keys()
    async def aio_get(self, sound_uuid: str): return self.sounds.get(sound_uuid)
    async def aio_add(self, sound: Sound): self.sounds[(sound_uuid:=str(uuid.uuid4()))] = sound ; return sound_uuid
import os
import asyncio
import aiofiles
from io import BytesIO
# > Image Works
from PIL import Image
# > Sound Works
try:
    from playsoundsimple import Sound
    SOUND_IMPORTED = True
except:
    SOUND_IMPORTED = False
# > Typing
from typing import Literal, Tuple, Optional, Iterable, TypeVar

# ! Types
T = TypeVar("T")

# ! Async Functions
async def aiter(it: Iterable[T]):
    for i in it:
        await asyncio.sleep(0)
        yield i

async def get_bar_status() -> Tuple[str, Optional[float], Optional[float]]: return "", None, None

async def aio_is_midi_file(filepath: str):
    async with aiofiles.open(filepath, 'rb') as file:
        return await file.read(4) == b"MThd"

# ! Functions
if SOUND_IMPORTED:
    def check_status(sound: Sound) -> Literal["Stoped", "Playing", "Paused"]:
        if sound.playing:
            if sound.paused: return "Paused"
            else: return "Playing"
        return "Stoped"

    def get_sound_basename(sound: Sound) -> str:
        if sound.title is not None:
            if sound.artist is not None:
                return f"{sound.artist} - {sound.title}"
            return f"{sound.title}"
        return f"{os.path.basename(sound.name)}"

def image_from_bytes(data: Optional[bytes]) -> Optional[Image.Image]:
    if data is not None: return Image.open(BytesIO(data))

def is_midi_file(filepath: str) -> bool:
    with open(filepath, 'rb') as file:
        return file.read(4) == b"MThd"

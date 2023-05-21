import os
import asyncio
import aiofiles
from io import BytesIO
# > Image Works
from PIL import Image
# > Typing
from typing import Literal, Tuple, Optional, Iterable, TypeVar
# > Local Imports
from .codeсbase import CodecBase

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

# ! Exceptions Rich
def rich_exception(exc: Exception) -> str:
    return f"[red]{exc.__class__.__name__}[/red]: {exc.__str__()}"

# ! Functions
def check_status(sound: CodecBase) -> Literal["Stoped", "Playing", "Paused"]:
    if sound.playing:
        if sound.paused: return "Paused"
        else: return "Playing"
    return "Stoped"

def get_sound_basename(sound: CodecBase) -> str:
    if sound.title is not None:
        if sound.artist is not None:
            return f"{sound.artist} - {sound.title}"
        return f"{sound.title}"
    try: return f"{os.path.basename(sound.name)}"
    except: return sound.name

def image_from_bytes(data: Optional[bytes]) -> Optional[Image.Image]:
    if data is not None: return Image.open(BytesIO(data))
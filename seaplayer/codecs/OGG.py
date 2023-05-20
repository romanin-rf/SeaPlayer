import aiofiles
# > Local Imports
from .MP3 import MP3Codec


class OGGCodec(MP3Codec):
    codec_name: str = "OGG"
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, "rb") as file:
            return file.read(4) == b'OggS'
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, "rb") as file:
            return await file.read(4) == b'OggS'

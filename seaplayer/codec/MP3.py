import aiofiles
# > Local Imports
from .Any import AnyCodec


class MP3Codec(AnyCodec):
    codec_name: str = "MP3"
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, "rb") as file:
            return file.read(3) == b'ID3'
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, "rb") as file:
            return await file.read(3) == b'ID3'

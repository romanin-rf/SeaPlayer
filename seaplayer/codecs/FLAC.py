import aiofiles
# > Local Imports
from .Any import AnyCodec


class FLACCodec(AnyCodec):
    codec_name: str = "FLAC"
    
    # ! Testing
    @staticmethod
    def is_this_codec(path: str) -> bool:
        with open(path, "rb") as file:
            return file.read(4) == b'fLaC'
    
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool:
        async with aiofiles.open(path, "rb") as file:
            return await file.read(4) == b'fLaC'

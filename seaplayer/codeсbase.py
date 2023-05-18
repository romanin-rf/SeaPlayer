from typing import Optional

# ! Codecs Base
class CodecBase:
    # * Codec Info
    codec_name: str
    
    # * Info
    name: str
    duration: float
    channels: int
    samplerate: int
    bitrate: int
    
    # * Sound Info
    title: Optional[str]
    artist: Optional[str]
    album: Optional[str]
    icon_data: Optional[bytes]
    
    # * Playback Info
    playing: bool
    paused: bool
    
    # ! Initializing Functions
    def __init__(self, path: str, **kwargs) -> None: ...
    
    def __sha1__(self, buffer_size: int) -> str: ...
    async def __aio_sha1__(self, buffer_size: int) -> str: ...
    
    # ! Testing Functions
    @staticmethod
    def is_this_codec(path: str) -> bool: return False
    @staticmethod
    async def aio_is_this_codec(path: str) -> bool: return False
    
    # ! Playback Functions
    def play(self) -> None: ...
    def stop(self) -> None: ...
    def pause(self) -> None: ...
    def unpause(self) -> None: ...
    def get_volume(self) -> float: return 1.0
    def set_volume(self, value: float) -> None: ...
    def get_pos(self) -> float: return 0.0
    def set_pos(self, value: float) -> None: ...

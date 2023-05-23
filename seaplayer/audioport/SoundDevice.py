import asyncio
import numpy as np
import sounddevice as sd
# > Typing Import
from typing import NoReturn, Optional, Tuple, Union, Literal
# > Local Import's
from ..audioportbase import AudioPortBase

# ! Types
DATA = np.ndarray[Tuple[int, int]]
VOLUME = float
CODE = Literal[0]

# ! Main Class
class SoundDeviceAudioPort(AudioPortBase):
    audio_port_name: str = "SoundDevice"
    
    def __init__(
        self,
        channels: int=2,
        samplerate: int=44100,
        dtype: str="float32",
        device_id: Optional[int]=None,
        *args, **kwargs
    ) -> None:
        self.queue: asyncio.Queue[Union[DATA, CODE]] = asyncio.Queue(1)
        self.device_id: int = device_id
        self.channels: int = channels
        self.samplerate: int = samplerate
        self.dtype: str = dtype
        self.streaming: bool = False
    
    async def loop(self) -> None:
        with sd.OutputStream(samplerate=self.samplerate, device=self.device_id, channels=self.channels, dtype=self.dtype) as stream:
            while self.streaming:
                data = await self.queue.get()
                if isinstance(data, int):
                    if data == 0:
                        self.streaming = False
                        break
                else:
                    stream.write(data)
    
    async def send_data(self, data: Union[DATA, CODE]) -> None:
        await self.queue.put(data)
    
    async def start(self) -> NoReturn:
        self.streaming = True
        await self.loop()
    
    async def stop(self) -> None:
        self.streaming = False
        await self.queue.put(0)
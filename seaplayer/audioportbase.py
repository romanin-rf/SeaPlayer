from typing import Any, NoReturn

class AudioPortBase:
    audio_port_name: str = "AudioPort"
    
    def __init__(self, *args, **kwargs) -> None: pass
    
    async def send_data(self, data: Any) -> None: pass
    
    async def start(self) -> NoReturn: pass
    async def stop(self) -> None: pass
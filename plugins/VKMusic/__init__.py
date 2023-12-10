import logging
from rich.console import Console
from rich.prompt import Prompt
from seaplayer.plug import PluginBase
from vkpymusic import Service, TokenReceiver
# > Local Imports
from .vkmcodec import VKMCodec
from .units import (
    pcheck,
    VKM_MAIN_PATTERN,
    VKM_RANGE_PATTERN
)

# ! Logging Disable
logging.disable()

# ! Vars
console = Console()

# ! Plugin Value Hander
def vkm_value_handler(value: str):
    values = []
    if (d:=pcheck(VKM_RANGE_PATTERN, value)) is not None:
        for i in range(d['ssid'], d['esid']):
            values.append(f"vkm://{d['uid']}/{i}")
    return values

# ! Plugin Class
class VKMusic(PluginBase):
    def exist_token(self) -> bool:
        if (s:=Service.parse_config()) is not None:
            del s
            return True
        else:
            return False
    
    def on_init(self) -> None:
        self.configurated = self.exist_token()
    
    def on_run(self) -> None:
        if self.configurated:
            self.service = Service.parse_config()
        else:
            login, password = Prompt.ask("Login"), Prompt.ask("Password", password=True)
            while not self.configurated:
                tr = TokenReceiver(login, password)
                if tr.auth(on_2fa=lambda: Prompt.ask("Code 2FA")):
                    tr.save_to_config()
                    self.configurated = True
                else:
                    console.print("[red]Failed to get a token, repeat...[/red]")
            self.service = Service.parse_config()
        self.app.info(f"Service is worked: {repr(self.service)}")
        # ! Registration
        self.app.CODECS_KWARGS["vkm_service"] = self.service
        self.add_value_handlers(vkm_value_handler)
        self.add_codecs(VKMCodec)

# ! Registeration
__plugin__ = VKMusic
import logging
from textual.widgets import Input, Label
from textual.containers import Center
from seaplayer.plug import PluginBase
from seaplayer.objects import PopUpWindow, WaitButton
from vkpymusic import Service, TokenReceiverAsync
# > Typing
from typing import Tuple
# > Local Imports
from .vkmcodec import VKMCodec
from .units import (
    pcheck,
    VKM_RANGE_PATTERN
)

# ! Logging Disable
logging.disable()

# ! Plugin Class
class VKMusic(PluginBase):
    def vkm_value_handler(self, value: str):
        values = []
        if (d:=pcheck(VKM_RANGE_PATTERN, value)) is not None:
            for i in range(d['ssid'], d['esid']):
                values.append(f"vkm://{d['uid']}/{i}")
        return values
    
    def exist_token(self) -> bool:
        if (s:=Service.parse_config()) is not None:
            del s
            return True
        else:
            return False
    
    # ? For user requests methods
    async def __req_login_password(self) -> Tuple[str, str]:
        lppw = PopUpWindow(
            ilogin:=Input(placeholder="Login"),
            ipassword:=Input(placeholder="Password", password=True),
            Center(elpb:=WaitButton("Log In")),
            title="VKMusic Authentication"
        )
        await self.app.mount(lppw)
        await elpb.wait_click()
        login, password = ilogin.value, ipassword.value
        await lppw.remove()
        return login, password
    
    async def __req_2fa(self) -> str:
        cpw = PopUpWindow(
            icode:=Input(placeholder="Code"),
            Center(ecb:=WaitButton("Enter")),
            title="VKMusic Authentication"
        )
        await self.app.mount(cpw)
        await ecb.wait_click()
        code = icode.value
        await cpw.remove()
        return code
    
    async def __req_capcha(self, url: str) -> str:
        cpw = PopUpWindow(
            Label(f"[link={url}]{url}[/link]"),
            icapcha:=Input(placeholder="Capcha"),
            Center(ecb:=WaitButton("Enter")),
            title="VKMusic Authentication"
        )
        await self.app.mount(cpw)
        await ecb.wait_click()
        code = icapcha
        await cpw.remove()
        return code
    
    async def __req_invalid_client(self) -> None:
        pass
    
    async def __req_critical_error(self) -> None:
        pass
    
    async def __init_service__(self) -> None:
        if self.configurated:
            self.service = Service.parse_config()
        else:
            while not self.configurated:
                login, password = await self.__req_login_password()
                tr = TokenReceiverAsync(login, password)
                if await tr.auth(
                    self.__req_capcha,
                    self.__req_2fa,
                    self.__req_invalid_client,
                    self.__req_critical_error
                ):
                    tr.save_to_config()
                    self.configurated = True
                else:
                    self.app.error("Failed to get a token, repeat...")
            self.service = Service.parse_config()
        self.app.info(f"Service is worked: {repr(self.service)}")
        # ? Registration
        self.app.CODECS_KWARGS.update({"vkm_service": self.service})
        self.add_value_handlers(self.vkm_value_handler)
        self.add_codecs(VKMCodec)
    
    def on_init(self) -> None:
        self.configurated = self.exist_token()
    
    async def on_ready(self):
        self.app.run_worker(self.__init_service__, group=self.info.name_id)

# ! Registeration
__plugin__ = VKMusic

import logging
from textual.widgets import Input, Label
from textual.containers import Center
from seaplayer.plug import PluginBase
from seaplayer.objects import PopUpWindow, WaitButton
from vkpymusic import Service, TokenReceiverAsync
# > Typing
from typing import Optional, Tuple, List
# > Local Imports
from .vkmcodec import VKMCodec
from .units import (
    pget,
    VKM_RANGE_SUID_PATTERN,
    VKM_TEXT_PATTERN,
    VKM_TEXT_RANGE_PATTERN,
)

# ! Logging Disable
logging.disable()

# ! Plugin Class
class VKMusic(PluginBase):
    def vkm_value_handler(self, value: str) -> List[str]:
        values = []
        if self.service is not None:
            # "vkm://users/<uid:int>:<ssid:int>-<esid:int>"
            if (d:=pget(VKM_RANGE_SUID_PATTERN, value)) is not None:
                for sid in range(d['ssid'], d['esid']):
                    values.append(f"vkm://users/{d['uid']}:{sid}") # > "vkm://users/<uid:int>:<sid:int>"
            # "vkm://songs:<text>:<count:int>"
            elif (d:=pget(VKM_TEXT_RANGE_PATTERN, value)) is not None:
                for offset in range(d['count']):
                    values.append(f"vkm://songs:{d['text']}:1:{offset}") # > "vkm://songs:<text>:<count:int>:<offset:int>"
            # "vkm://songs:<text>"
            elif (d:=pget(VKM_TEXT_PATTERN, value)) is not None:
                values.append(f"vkm://songs:{d['text']}:1:0") # > "vkm://songs:<text>:<count:int>:<offset:int>"
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
        self.service: Optional[Service] = None
        self.configurated = self.exist_token()
    
    async def on_ready(self):
        self.app.run_worker(self.__init_service__, group=self.info.name_id)

# ! Registeration
__plugin__ = VKMusic

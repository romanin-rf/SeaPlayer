import os
import time
import asyncio
import nest_asyncio
from pypresence import Presence, DiscordNotFound
from seaplayer.plug import PluginBase

# ! Vars
AD_ENABLE = True

# ! Initialization
nest_asyncio.apply()

# ! Main Class
class RichDiscordStatus(PluginBase):
    def get_status(self):
        data = {
            "start": self.start_time,
            "large_image": "icon"
        }
        if AD_ENABLE:
            data["buttons"] = [{"label": "GitHub", "url": self.info.url}]
        if self.app.currect_sound is not None:
            if (self.app.currect_sound.title is not None) and (self.app.currect_sound.artist is not None):
                data["details"] = f"{self.app.currect_sound.artist} - {self.app.currect_sound.title}"
            else:
                data["details"] = os.path.basename(self.app.currect_sound.name)
            if self.app.currect_sound.paused:
                data["state"] = "Paused"
            elif self.app.currect_sound.playing:
                data["state"] = "Playing"
            else:
                data["state"] = "Stopped"
        else:
            data["details"] = "Sound not selected"
            data["state"] = "Waiting"
        return data
    
    async def __status__(self) -> None:
        while self.running:
            try:
                rpc = Presence("1178379471124955217")
                rpc.connect()
                while self.running:
                    rpc.update(**self.get_status())
                    await asyncio.sleep(1)
            except DiscordNotFound:
                await asyncio.sleep(10)
    
    def on_run(self) -> None:
        self.start_time = time.time()
    
    async def on_compose(self):
        self.running = True
        self.app.run_worker(self.__status__, "Discord Rich Status", "seaplayer.plugins.discord.status", thread=True)
    
    async def on_quit(self) -> None:
        self.running = False

# ! Registration Plugin Class
plugin_main = RichDiscordStatus
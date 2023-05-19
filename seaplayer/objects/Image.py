from textual.widgets import Label
# > Image Works
from PIL import Image
from PIL.Image import Resampling
from ripix import AsyncPixels, Pixels
# > Typing
from typing import Optional, Union, Tuple


class StandartImageLabel(Label):
    def __init__(
        self,
        default_image: Image.Image,
        image: Optional[Image.Image]=None,
        fps: int=2,
        *,
        resample: Resampling=Resampling.NEAREST
    ):
        super().__init__("<image not found>", classes="image-label")
        self.image_resample = resample
        self.default_image: Image.Image = default_image
        self.image: Optional[Image.Image] = image
        self.image_text: Union[str, Pixels] = "<image not found>"
        self.last_image_size: Optional[Tuple[int, int]] = None
        self._fps = fps
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/self._fps, self.update_image_label)
    
    async def update_image_label(self):
        image, resample = (self.default_image, Resampling.NEAREST) if (self.image is None) else (self.image, self.image_resample)
        
        new_size = (self.size[0], self.size[1])
        if self.last_image_size != new_size:
            self.image_text = Pixels.from_image(image, new_size, resample)
            self.last_image_size = new_size
        
        self.update(self.image_text)
    
    async def update_image(self, image: Optional[Image.Image]=None) -> None:
        self.image = image
        
        image, resample = (self.default_image, Resampling.NEAREST) if (self.image is None) else (self.image, self.image_resample)
        self.image_text = Pixels.from_image(image, (self.size[0], self.size[1]), resample)

class AsyncImageLabel(Label):
    def __init__(
        self,
        default_image: Image.Image,
        image: Optional[Image.Image]=None,
        fps: int=2,
        *,
        resample: Resampling=Resampling.NEAREST
    ):
        super().__init__("<image not found>", classes="image-label")
        self.image_resample = resample
        self.default_image: Image.Image = default_image
        self.image: Optional[Image.Image] = image
        self.image_text: Union[str, AsyncPixels] = "<image not found>"
        self.last_image_size: Optional[Tuple[int, int]] = None
        self._fps = fps
    
    def on_mount(self) -> None:
        self.update_render = self.set_interval(1/self._fps, self.update_image_label)
    
    async def update_image_label(self):
        image, resample = (self.default_image, Resampling.NEAREST) if (self.image is None) else (self.image, self.image_resample)
        
        new_size = (self.size[0], self.size[1])
        if self.last_image_size != new_size:
            self.image_text = await AsyncPixels.from_image(image, new_size, resample)
            self.last_image_size = new_size
        
        self.update(self.image_text)
    
    async def update_image(self, image: Optional[Image.Image]=None) -> None:
        self.image = image
        
        image, resample = (self.default_image, Resampling.NEAREST) if (self.image is None) else (self.image, self.image_resample)
        self.image_text = await AsyncPixels.from_image(image, (self.size[0], self.size[1]), resample)
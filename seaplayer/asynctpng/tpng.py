import io
import asyncio
import aiofiles
from pathlib import Path
from tempfile import mkstemp
from PIL import Image
from typing import Optional, Iterable, TypeVar

# ! Types
T = TypeVar("T")

# ! Functions
async def aiter(it: Iterable[T]):
    for i in it:
        yield i
        await asyncio.sleep(0)

async def arange(*args):
    for i in range(*args):
        yield i
        await asyncio.sleep(0)

async def aio_get_image(fp) -> Optional[Path]:
    if isinstance(fp, Path) or isinstance(fp, str):
        path = Path(fp)
    elif isinstance(fp, bytes):
        path = Path(mkstemp())
        async with aiofiles.open(path, "wb") as file:
            await file.write(fp)
    elif isinstance(fp, io.BytesIO) or isinstance(fp, io.BufferedIOBase):
        path = Path(mkstemp())
        fp.seek(0)
        async with aiofiles.open(path, "wb") as to_file:
            await to_file.write(fp.read())
    else: path = None
    
    if path is not None:
        if path.exists() and path.is_file(): return path

def get_image(fp) -> Optional[Path]:
    if isinstance(fp, Path) or isinstance(fp, str):
        path = Path(fp)
    elif isinstance(fp, bytes):
        path = Path(mkstemp())
        with open(path, "wb") as file: file.write(fp)
    elif isinstance(fp, io.BytesIO) or isinstance(fp, io.BufferedIOBase):
        path = Path(mkstemp())
        fp.seek(0)
        with open(path, "wb") as to_file: to_file.write(fp.read())
    else: path = None
    
    if path is not None:
        if path.exists() and path.is_file(): return path

# ! Main Class
class AsyncTPNG:
    def __init__(
        self,
        fp,
        *args,
        **kwargs
    ) -> None:
        if fp is not None:
            if not isinstance(fp, Image.Image):
                self.image_path = get_image(fp)
                if self.image_path is None: raise RuntimeError(f"Failed to get '~PIL.Image.Image'.")
                self.image = Image.open(self.image_path, *args, **kwargs)
            else:
                self.image = fp
            
            if self.image.mode != "RGB": self.image = self.image.convert("RGB")
            self.use_image: Image.Image = self.image.copy()
        else:
            self.image: Image.Image = None
            self.use_image: Image.Image = None
    
    @staticmethod
    async def async_init(
        fp,
        *args,
        **kwargs
    ) -> None:
        if not isinstance(fp, Image.Image):
            image_path = await aio_get_image(fp)
            if image_path is None: raise RuntimeError(f"Failed to get '~PIL.Image.Image'.")
            image = Image.open(image_path, *args, **kwargs)
        else:
            image = fp
    
        if image.mode != "RGB": image = image.convert("RGB")
        use_image: Image.Image = image.copy()
        
        async_tpng = AsyncTPNG(None)
        async_tpng.image = image
        async_tpng.use_image = use_image
        return async_tpng
    
    @staticmethod
    async def to_hex(pixel: Iterable[int]) -> str: return "#"+"".join([hex(i)[2:].rjust(2,"0") async for i in aiter(pixel)])
    
    @property
    def size(self): return self.use_image.size
    
    async def resize(self, size: tuple) -> None: self.use_image = self.use_image.resize(size)
    async def convert(self, mode: str) -> None: self.use_image = self.use_image.convert(mode)
    async def reset(self) -> None: self.use_image = self.image.copy()
    
    async def to_rich_image(
        self,
        pixel: str="█",
        error_pixel: str="?",
        alpha_pixel: str=" ",
        alpha_colors: list=[]
    ) -> str:
        timg = ""
        img = self.use_image if self.use_image.mode == "RGB" else self.use_image.convert("RGB")
        
        async for y in arange(img.size[1]):
            async for x in arange(img.size[0]):
                pix = img.getpixel((x, y))
                if pix not in alpha_colors:
                    hex_pix = await self.to_hex(pix)
                    timg += f"[{hex_pix}]{pixel}[/]"
                else:
                    timg += alpha_pixel
            timg += "\n"
        return timg

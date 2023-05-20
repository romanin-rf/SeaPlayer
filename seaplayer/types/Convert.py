from pathlib import Path
# > Typing
from typing import Optional, Tuple, Any
# > Local Import's
from ..exceptions import (
    PathNotExistsError,
    NotBooleanError
)

class Converter:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
    
    @staticmethod
    def conv(tp: type, value: str) -> Tuple[bool, Optional[Any]]:
        try: return True, tp(value)
        except: return False, None
    
    @staticmethod
    async def aio_conv(tp: type, value: str) -> Tuple[bool, Optional[Any]]:
        try: return True, tp(value)
        except: return False, None
    
    def gen_conv(self, tp: type):
        def conv_wrapper(value: str) -> Tuple[bool, Optional[Any]]:
            return self.conv(tp, value)
        return conv_wrapper
    
    def gen_aio_conv(self, tp: type):
        async def aio_conv_wrapper(value: str) -> Tuple[bool, Optional[Any]]:
            return await self.aio_conv(tp, value)
        return aio_conv_wrapper
    
    # ! Convert Types
    @staticmethod
    def path(value: str) -> str:
        """Checking the existence of a `path`."""
        if not Path(value).exists(): raise PathNotExistsError(value)
        return value
    
    @staticmethod
    def filepath(value: str) -> str:
        """Check if there is a file on the path."""
        path = Path(value)
        if not(path.exists() and path.is_file()): raise PathNotExistsError(value)
        return value
    
    @staticmethod
    def boolean(value: str) -> bool:
        """Converting to `bool`."""
        if value.lower() == "true": return True
        elif value.lower() == "false": return False
        else: raise NotBooleanError(value)
    
    @staticmethod
    def optional(tp: type):
        """This is a type or function decorator for converting a value."""
        def optional_wrapper(value: str):
            if value.lower() != "none":
                return tp(value)
        return optional_wrapper
    
    @staticmethod
    def union(*tps: type):
        def union_wrapper(value: str):
            for tp in tps:
                try: return tp(value)
                except: pass
            raise TypeError(f"Could not convert to any of the listed types: {tps}")
        return union_wrapper
    
    @staticmethod
    def literal_string(*values: str):
        def literal_string_wrapper(value: str):
            if value in values: return value
            raise RuntimeError(f"The value ({repr(value)}) is not in the list of values.")
        return literal_string_wrapper
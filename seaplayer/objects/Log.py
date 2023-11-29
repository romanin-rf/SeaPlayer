from rich.console import Console
from textual.widgets import RichLog
# > Typing
from typing import TypeVar
# > Local Import's
from ..functions import rich_exception

# ! Vars
console = Console()

# ! Types
RETURN = TypeVar('RETURN')

# ! Main Class
class LogMenu(RichLog):
    def __init__(self, chap_max_width: int=8, enable_logging: bool=True, **kwargs):
        self.enable_logging = enable_logging
        self.chap_max_width = chap_max_width
        
        if kwargs.get("classes", None) is not None:
            kwargs["classes"] = kwargs["classes"] + " log-menu -hidden"
        else:
            kwargs["classes"] = "log-menu -hidden"
        
        super().__init__(**kwargs)
    
    def write_log(self, chap: str, msg: str, *, chap_color: str="green", in_console: bool=False) -> None:
        if self.enable_logging:
            text = f"[[{chap_color}]{chap.center(self.chap_max_width)}[/]]: {msg}"
            self.write(text, shrink=False)
            if in_console:
                console.print(text)
    
    def info(self, msg: str, *, in_console: bool=False) -> None:
        self.write_log("INFO", msg, chap_color="green", in_console=in_console)
    
    def error(self, msg: str, *, in_console: bool=False) -> None:
        self.write_log("ERROR", msg, chap_color="red", in_console=in_console)
    
    def warn(self, msg: str, *, in_console: bool=False) -> None:
        self.write_log("WARN", msg, chap_color="orange", in_console=in_console)
    
    def exception(self, e: Exception, *, in_console: bool=False) -> None:
        self.write_log("ERROR", rich_exception(e), chap_color="red", in_console=in_console)

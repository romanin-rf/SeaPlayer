from textual.widgets import TextLog


class LogMenu(TextLog):
    def __init__(self, chap_max_width: int=8, enable_logging: bool=True, **kwargs):
        self.enable_logging = enable_logging
        self.chap_max_width = chap_max_width
        
        if kwargs.get("classes", None) is not None:
            kwargs["classes"] = kwargs["classes"] + " log-menu -hidden"
        else:
            kwargs["classes"] = "log-menu -hidden"
        
        super().__init__(**kwargs)
    
    def write_log(self, chap: str, msg: str, *, chap_color: str="green") -> None:
        if self.enable_logging: self.write(f"[[{chap_color}]{chap.center(self.chap_max_width)}[/]]: {msg}", shrink=False)
    
    def info(self, msg: str) -> None: self.write_log("INFO", msg, chap_color="green")
    def error(self, msg: str) -> None: self.write_log("ERROR", msg, chap_color="red")
    def warn(self, msg: str) -> None: self.write_log("WARN", msg, chap_color="orange")
from typing import Generator, Optional, Iterable, Any

# ! Error Base Class
class Error(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.args = [i for i in self.__error_text__(*args, **kwargs) if i is not None]
    
    def __error_text__(self, *args, **kwargs) -> Generator[Optional[str], Any, None]:
        yield None

# ! Language Errors
class LanguageNotExistError(Error):
    def __error_text__(self, marks: Iterable[str], *args, **kwargs):
        yield f"No language file(s) with such a mark(s) was found: {', '.join([repr(mark) for mark in marks])}"

class LanguageNotLoadedError(Error):
    def __error_text__(self, *args, **kwargs):
        yield f"The language file has not been uploaded. Use the `load` method."

# ! Exceptions
class PathNotExistsError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.args = (f"The element along the path {repr(path)} does not exist.",)

class NotBooleanError(Exception):
    def __init__(self, data: str) -> None:
        super().__init__()
        self.args = (f"The data {repr(data)} cannot be represented as a bool.",)
class PathNotExistsError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.args = (f"The element along the path {repr(path)} does not exist.",)

class NotBooleanError(Exception):
    def __init__(self, data: str) -> None:
        super().__init__()
        self.args = (f"The data {repr(data)} cannot be represented as a bool.",)
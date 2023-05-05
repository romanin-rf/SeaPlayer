class PathNotExistsError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.args = (f"The element along the path '{path}' does not exist.",)

class NotBooleanError(Exception):
    def __init__(self, data: str) -> None:
        super().__init__()
        self.args = (f"The data '{data}' cannot be represented as a bool.",)
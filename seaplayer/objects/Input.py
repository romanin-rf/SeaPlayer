from textual.widgets import Input
# > Typing
from typing import Optional, Tuple, Any

# ! InputFiles functions
async def _conv(value: str) -> Tuple[bool, Optional[Any]]: return True, value
async def _submit(input: Input, value: Any) -> None: ...
def _update_placeholder() -> Optional[str]: ...

# ! InputField class
class InputField(Input):
    def __init__(
        self,
        conv=_conv,
        submit=_submit,
        update_placeholder=_update_placeholder,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._conv = conv
        self._submit = submit
        self._update_placeholder = update_placeholder
        if (placeholder:=self._update_placeholder()) is not None:
            self.placeholder = placeholder
    
    async def action_submit(self):
        value = self.value
        self.value = ""
        if value.replace(" ", "") != "":
            ok, c_value = await self._conv(value)
            if ok: await self._submit(self, c_value)
        if (placeholder:=self._update_placeholder()) is not None:
            self.placeholder = placeholder
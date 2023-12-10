from vbml import Pattern, Patcher
# > Typing
from typing import Optional, Dict, Any

# ! VBML Objects
PATCHER = Patcher()

VKM_MAIN_PATTERN = Pattern("vkm://<uid:int>/<sid:int>")
VKM_RANGE_PATTERN = Pattern("vkm://<uid:int>/<ssid:int>-<esid:int>")

# ! For VBML methods
def pcheck(pattern: Pattern, text: str) -> Optional[Dict[str, Any]]:
    if isinstance(data:=PATCHER.check(pattern, text), dict):
        return data
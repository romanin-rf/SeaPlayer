from vbml import Pattern, Patcher
# > Typing
from typing import Optional, Dict, Any

# ! VBML Objects
PATCHER = Patcher()

VKM_SUID_PATTERN =                  Pattern("vkm://users/<uid:int>:<sid:int>")              # ! vkmcodec
VKM_RANGE_SUID_PATTERN =            Pattern("vkm://users/<uid:int>:<ssid:int>-<esid:int>")  # > vkm_value_handler
VKM_TEXT_PATTERN =                  Pattern("vkm://songs:<text>")                           # > vkm_value_handler
VKM_TEXT_RANGE_PATTERN =            Pattern("vkm://songs:<text>:<count:int>")               # > vkm_value_handler
VKM_TEXT_RANGE_OFFSET_PATTERN =     Pattern("vkm://songs:<text>:<count:int>:<offset:int>")  # ! vkmcodec

# ! For VBML methods
def pget(pattern: Pattern, text: str) -> Optional[Dict[str, Any]]:
    if isinstance(data:=PATCHER.check(pattern, text), dict):
        return data

def pcheck(pattern: Pattern, text: str) -> bool:
    return isinstance(PATCHER.check(pattern, text), dict)

def pchecks(text: str, *patterns: Pattern) -> bool:
    return max([pcheck(pattern, text) for pattern in patterns])
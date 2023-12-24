from typing import TypeVar, Generic, Optional, Dict

# ! Types
T = TypeVar('T')
K = TypeVar('K')
G = TypeVar('G')

# ! Main Class
class Environment(Generic[G, K, T]):
    def __init__(
        self,
        setup_data: Dict[G, Dict[K, T]]={}
    ) -> None:
        self.env: Dict[G, Dict[K, T]] = setup_data
    
    # ? Magic Methods
    def __str__(self) -> str:
        return str(self.env)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.env)})"
    
    def __getitem__(self, group: K) -> Dict[K, T]:
        if group not in list(self.env.keys()):
            self.env[group] = {}
        return self.env[group]
    
    def __setitem__(self, group: K, value: Dict[K, T]) -> None:
        assert isinstance(value, dict)
        self.env[group] = value
    
    # ? Main Methods
    def set(self, group: G, key: K, value: T) -> None:
        if group not in list(self.env.keys()):
            self.env[group] = {}
        self.env[group][key] = value
    
    def get(self, group: G, key: K, default: Optional[T]=None) -> Optional[T]:
        if group in list(self.env.keys()):
            return self.env[group].get(key, default)
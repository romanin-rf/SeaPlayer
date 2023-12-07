import os
import glob
import properties
from typing import Dict, Tuple, Optional
# > Local Imports
from .functions import formater
from .exceptions import LanguageNotExistError, LanguageNotLoadedError

# ! Child Class
class Language:
    @staticmethod
    def __load_file(filepath: str) -> Dict[str, str]:
        with open(filepath, 'r', errors='ignore', encoding='utf-8') as file:
            return properties.load(file)
    
    def __get_metadata(self) -> Tuple[str, str, Optional[str], Dict[str, str]]:
        data = self.__load_file(self.__name)
        return \
            data.get("language.metadata.title", f"<LTNF:{self.__mark}>"), \
            data.get("language.metadata.author", "<unknown>"), \
            data.get("language.metadata.author.url", None), \
            {
                "from": data.get("language.metadata.words.from", "from")
            }
    
    # ? Initialization
    def __init__(self, language_filepath: str) -> None:
        self.__name = os.path.abspath(language_filepath)
        self.__data, self.__loaded = None, False
        # * Checking
        if not os.path.isfile(self.__name):
            raise FileNotFoundError
        # * Metadata Loading
        self.__mark = os.path.splitext(os.path.basename(self.__name))[0].lower()
        self.__title, self.__author, self.__author_url, self.__words = self.__get_metadata()
    
    # ? Magic Methods
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({formater(name=self.__name, title=self.__title, mark=self.__mark)})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ? Propertyes
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def mark(self) -> str:
        return self.__mark
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def author(self) -> str:
        return self.__author
    
    @property
    def author_url(self) -> str:
        return self.__author_url
    
    @property
    def words(self) -> Dict[str, str]:
        return self.__words
    
    @property
    def loaded(self) -> bool:
        return self.__loaded
    
    # ? Main Methods
    def load(self) -> None:
        self.__data, self.__loaded = self.__load_file(self.__name), True
    
    def unload(self) -> None:
        self.__data, self.__loaded = None, False
    
    def get(self, key: str, default: Optional[str]=None) -> Optional[str]:
        if self.loaded:
            return self.__data.get(key, default)
        raise LanguageNotLoadedError()

# ! Main Class
class LanguageLoader:
    # ? Main Methods
    def __search_langs(self, dlm: str, mlm: str) -> Tuple[Language, Language]:
        dl, ml = None, None
        for lang in self.langs:
            if lang.mark == dlm:
                dl = lang
            if lang.mark == mlm:
                ml = lang
        if (dl is None) or (ml is None):
            raise LanguageNotExistError([dlm, mlm])
        dl.load()
        ml.load()
        return dl, ml
    
    # ? Initialization
    def __init__(
        self,
        langs_dirpath: str,
        main_lang_mark: str,
        default_lang_mark: str="en-eng",
    ) -> None:
        self.__name = os.path.abspath(langs_dirpath)
        self.__mlm = main_lang_mark.lower()
        self.__dlm = default_lang_mark.lower()
        # * Checking
        if not os.path.isdir(self.__name):
            raise FileNotFoundError
        # * Searching Languages
        self.langs = [Language(lp) for lp in glob.glob(os.path.join(self.__name, "??-???.properties"))]
        self.dlang, self.mlang = self.__search_langs(self.__dlm, self.__mlm)
    
    def get(self, key: str) -> str:
        return self.mlang.get(key, self.dlang.get(key, "<LTNF>"))

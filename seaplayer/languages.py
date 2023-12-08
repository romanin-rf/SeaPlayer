import os
import glob
import properties
from typing import Dict, List, Tuple, Optional
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
        form = formater(name=self.__name, title=self.__title, mark=self.__mark, loaded=self.__loaded)
        return f"{self.__class__.__name__}({form})"
    
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
    def __search_langs(self, dlm: str, mlm: str) -> Tuple[Language, Optional[Language]]:
        dl, ml = None, None
        for lang in self.langs:
            if lang.mark == dlm:
                dl = lang
            if lang.mark == mlm:
                ml = lang
        if dl is None:
            raise LanguageNotExistError([dl])
        dl.load()
        if ml is not None:
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
        self.__alangs: List[LanguageLoader] = []
        # * Checking
        if not os.path.isdir(self.__name):
            raise FileNotFoundError
        # * Searching and loading languages
        self.__langs: List[Language] = [Language(lp) for lp in glob.glob(os.path.join(self.__name, "??-???.properties"))]
        self.__dlang, self.__mlang = self.__search_langs(self.__dlm, self.__mlm)
    
    # ? Magic Methods
    def __str__(self) -> str:
        form = formater(
            name=self.__name,
            default_lang_mark=self.__dlm,
            main_lang_mark=self.__mlm,
            langs=self.__langs,
            alangs=self.__alangs
        )
        return f"{self.__class__.__name__}({form})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    # ? Propertys
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def main_lang_mark(self) -> str:
        return self.__mlm
    
    @property
    def default_lang_mark(self) -> str:
        return self.__dlm
    
    @property
    def langs(self) -> List[Language]:
        return self.__langs
    
    @property
    def default_lang(self) -> Language:
        return self.__dlang
    
    @property
    def main_lang(self) -> Optional[Language]:
        return self.__mlang
    
    @property
    def alangs(self):
        """Additional languages, for example, translation of plugins.
        
        Returns:
            List[LanguageLoader]: A language loader with its own list of languages, which is the last thing to get from.
        """
        return self.__alangs
    
    # ? Public Methods
    def get(self, key: str) -> str:
        if self.__mlang is None:
            data = self.__dlang.get(key)
        data = self.__mlang.get(key, self.__dlang.get(key))
        if data is None:
            for alang in self.__alangs:
                if (data:=alang.get(key)) is not None:
                    break
        return data if data is not None else "<LTNF>"
    
    def merge(self, ll) -> None:
        assert isinstance(ll, LanguageLoader)
        self.__alangs.append(ll)
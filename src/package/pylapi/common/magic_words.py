from abc import ABC
import re

class MagicWords(ABC):
    def __init__(self, phrase: str):
        self.phrase = phrase
        _phrase = phrase
        _phrase = re.sub(r"[-_./]", " ", _phrase)
        _phrase = re.sub(r"([A-Z])", " \\1", _phrase)
        _phrase = re.sub(r" +", " ", _phrase)
        _phrase = _phrase.strip()
        self.words = [_.lower() for _ in _phrase.split(" ")]

    @property
    def snake(self) -> str:
        return "_".join(self.words)

    @property
    def kebab(self) -> str:
        return "-".join(self.words)

    @property
    def upperCamel(self) -> str:
        return "".join([_.capitalize() for _ in self.words])

    @property
    def lowerCamel(self) -> str:
        return self.words[0] + "".join([_.capitalize() for _ in self.words[1:]])

    @property
    def pascal(self) -> str:
        return self.upperCamel

    @property
    def camel(self) -> str:
        return self.lowerCamel

    @property
    def singular(self) -> str:
        _phrase = self.phrase
        _phrase = re.sub(r"ies$", "y", _phrase)
        _phrase = re.sub(r"ches$", "ch", _phrase)
        _phrase = re.sub(r"shes$", "sh", _phrase)
        _phrase = re.sub(r"s$", "", _phrase)
        return _phrase

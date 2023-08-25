from abc import ABC
from typing import Any
import json
from .dotted_dict import *
from .logger_util import *

# To handle path being non str
def _path_str(path):
    dotted_path = path
    if type(dotted_path) == int:
        dotted_path = f"$[{dotted_path}]"
    elif type(dotted_path) == slice:
        start = dotted_path.start if dotted_path.start != None else ""
        stop = dotted_path.stop if dotted_path.stop != None else ""
        step = dotted_path.step if dotted_path.step != None else ""
        dotted_path = f"$[{start}:{stop}:{step}]"
    return dotted_path


class pathDict(ABC):
    def __init__(self, data) -> None:
        self._data = data


    def __len__(self):
        return len(self._data)


    def __getattr__(self, attr) -> Any:
        logger.debug(f"__getattr__: {type(attr)} {attr}")
        return dotted_dict(self._data, attr)


    def __setattr__(self, attr, value: Any) -> None:
        logger.debug(f"__setattr__:  {type(attr)} {attr} <- {value}")
        # Use self.__dict__ to avoid recursion
        if not self.__dict__:
            # Init calling to set the first attribute (_data)
            self.__dict__[attr] = value
        elif "_data" not in self.__dict__:
            # Set the first _data attribute
            self._data = {attr: value}
        else:
            # self._data exists
            # self._data[attr] = value
            dotted_dict(self._data, attr, value=value)


    def __delattr__(self, attr: str) -> None:
        logger.debug(f"__delattr__: {type(attr)} {attr}")
        dotted_dict(self._data, attr, delete=True)
        # if "_data" in self.__dict__ and attr in self._data:
        #     del self._data[attr]


    def __getitem__(self, path) -> Any:
        logger.debug(f"__getitem__: {type(path)} {path}")
        return dotted_dict(self._data, _path_str(path))
        # if type(self._data[path]) != pathDict:
        #     return self._data[path]
        # else:
        #     val = pathDict(self._data[path])
        #     if val != None:
        #         return val
        #     else:
        #         return super().__getitem__(path)


    def __setitem__(self, path, value) -> Any:
        logger.debug(f"__setitem__: {type(path)} {path} <- {value}")
        # self._data[path] = value
        dotted_dict(self._data, _path_str(path), value=value)


    def __delitem__(self, path) -> Any:
        logger.debug(f"__delitem__: {type(path)} {path}")
        # del self._data[path]
        dotted_dict(self._data, _path_str(path), delete=True)


    def __str__(self) -> str:
        if type(self._data) == dict:
            return json.dumps(self._data)
        else:
            return str(self._data)


    def __repr__(self) -> str:
        # return str(self)
        return str(self._data)


    def __bool__(self) -> bool:
        return self._data != {}


    def __contains__(self, other) -> bool:
        # return other in self._data
        return self.__getitem__(other) != None


    def to_data(self):
        # logger.debug(f"to_data: {type(self._data)} {self._data}")
        return self._data


    def to_dict(self):
        # logger.debug(f"to_dict: {type(self._data)} {self._data}")
        return self._data


    def to_list(self):
        # logger.debug(f"to_list: {type(self._data)} {self._data}")
        return self._data

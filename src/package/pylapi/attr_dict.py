from abc import ABC
from typing import Any
import json
# import logging

# logging.basicConfig()
# logger = logging.getLogger()


class AttrDict(ABC):
    def __init__(self, data) -> None:
        self._data = data
        data_type = type(self._data)
        type_method_list = {}
        if data_type == dict:
            type_method_list = [
                "clear",
                "copy",
                "fromkeys",
                "get",
                "items",
                "keys",
                "pop",
                "popitem",
                "setdefault",
                "update",
                "values",
            ]
        elif data_type == list:
            type_method_list = [
                "append",
                "clear",
                "copy",
                "count",
                "extend",
                "index",
                "insert",
                "pop",
                "remove",
                "reverse",
                "sort",
            ]

        for type_method in type_method_list:
            self.__dict__[type_method] = self._type_method(data_type, type_method)


    def _type_method(self, type, method_name):
        def method_wrapper(*args, **kwargs):
            type_method = getattr(type, method_name)
            # logger.debug(type_method)
            return type_method(self.__dict__["_data"], *args, **kwargs)
        return method_wrapper


    def __len__(self):
        return len(self._data)


    def __getattr__(self, attr) -> Any:
        # logger.debug(f"__getattr__: {type(attr)} {attr}")
        if attr in self._data:
            if type(self._data[attr]) in (dict, list):
                return AttrDict(self._data[attr])
            else:
                return self._data[attr]
        else:
            raise Exception(f"{type(self).__name__} object has no attribute '{attr}'")


    def __setattr__(self, attr, value: Any) -> None:
        # logger.debug(f"__setattr__:  {type(attr)} {attr} <- {value}")
        # Use self.__dict__ to avoid recursion
        if not self.__dict__:
            # Init calling to set the first attribute (_data)
            self.__dict__[attr] = value
        elif "_data" not in self.__dict__:
            # Set the first _data attribute
            self._data = {attr: value}
        else:
            # self._data exists
            self._data[attr] = value


    def __delattr__(self, attr: str) -> None:
        # logger.debug(f"__getattr__: {type(attr)} {attr}")
        if "_data" in self.__dict__ and attr in self._data:
            del self._data[attr]


    def __getitem__(self, path) -> Any:
        # logger.debug(f"__getitem__: {type(path)} {path}")
        if type(self._data[path]) not in (dict, list):
            return self._data[path]
        else:
            val = AttrDict(self._data[path])
            if val != None:
                return val
            else:
                return super().__getitem__(path)


    def __setitem__(self, path, value) -> Any:
        # logger.debug(f"__setitem__: {type(path)} {path} <- {value}")
        self._data[path] = value


    def __delitem__(self, path) -> Any:
        # logger.debug(f"__delitem__: {type(path)} {path}")
        del self._data[path]


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

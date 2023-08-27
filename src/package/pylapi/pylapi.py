from __future__ import annotations
import functools

import json
import inspect

from abc import ABC
from typing import Any
from copy import deepcopy
from http import HTTPStatus

from .util.attr_dict import *
from .util.classproperty import *
from .util.config import *
from .util.error import *
from .util.logger_util import *
from .util.path_dict import *


# Convert path of int and slice types to str type to be used in dotted_dict
# This is to handle data being a non-str.
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


class PyLapiError(Exception):
    def __init__(self, api_response: dict):
        self.api_response = api_response
        self.message = "API response: " + str(self.api_response)
        super().__init__(self.message)


class PyLapi(ABC):
    # PyLapi class variables prefix: _pylapi_

    # User configurables
    _pylapi_auth = ""
    _pylapi_url = ""

    # API Requests
    _pylapi_auth_header_name = ""
    _pylapi_auth_type = ""
    _pylapi_base_headers = {}

    # API Classes and Routes
    _pylapi_resource_classes = {}
    _pylapi_resource_base_routes = {}

    # Callbacks
    _pylapi_callbacks = {}

    # Log
    _pylapi_log_level = config_log_level
    _pylapi_deep_log_level = config_deep_log_level

    def __init__(self, resource_data: dict = None, allow_api_raise=False) -> None:
        super().__init__()
        logger.debug(f"PyLapi.__init__(")
        logger.debug(f"    resource_data={resource_data},")
        logger.debug(f")")
        # logger.debug(f"for class {self.__class__.__dict__}")

        # Error handling
        self._allow_api_raise = allow_api_raise

        # Object attributes
        self._resource_data = resource_data if resource_data else {}

        self._request = None
        self._request_http_method = ""
        self._response = None
        self._response_data = {}


    ############################################################
    #
    # Protected methods - for subclasses and internal functions only
    #

    def _slash(self, string: str = "") -> str:
        return "/" + string if string else ""


    def _rewrite_data(self, rewrite, data: dict=None):
        _data = data if data else self._resource_data
        if type(rewrite) == str:
            # A path to data
            return PathDict(_data)[rewrite]

        rewrite_str = json.dumps(rewrite)
        rewrite_var_names = re.findall(r'"(\$[^"]*)"', rewrite_str)
        logger.debug(f"rewrite_var_names={rewrite_var_names}")
        for rewrite_var_name in rewrite_var_names:
            logger.debug(f"rewrite_var_name={rewrite_var_name}")
            rewrite_var_value = PathDict(_data)[rewrite_var_name]
            if type(rewrite_var_value) == str:
                rewrite_var_value = f'"{rewrite_var_value}"'
            elif type(rewrite_var_value) in (dict, list):
                rewrite_var_value = json.dumps(rewrite_var_value)
            else:
                rewrite_var_value = str(rewrite_var_value)
            rewrite_str = rewrite_str.replace(f'"{rewrite_var_name}"', rewrite_var_value)
        return json.loads(rewrite_str)


    def _obtain_request_args(
            self,
            method_route: str = "",
            data: dict = None,
            headers: dict = None,
            query: dict = None,
        ) -> dict:

        # _obtain_request_args(): GET resource route (with no query params)
        # _obtain_request_args(method_route): GET resource_base_route/method_route
        # _obtain_request_args(method_route,query=...): GET resource_base_route/method_route with query
        # _obtain_request_args(method_route,data=...,[query=...]): POST with data, with or without query
        # _obtain_request_args(method_route,data={},[query=...]): POST with data, with or without query

        # GET/POST above is indicative. The caller will determine if they get or post the request.

        # logger.debug(f"self._pylapi_url={self._pylapi_url}")
        # logger.debug(f"self._pylapi_resource_base_routes={self._pylapi_resource_base_routes}")
        # logger.debug(f"self._resource_name={self._resource_name}")
        # logger.debug(f"self._pylapi_base_headers={self.wash_secrets(self._pylapi_base_headers)}")
        logger.debug(f"_obtain_request_args: method_route={method_route}")
        api_url = f"{self._pylapi_url}{self._slash(self._pylapi_resource_base_routes[self._resource_name])}{self._slash(method_route)}"
        request = {
            "url": api_url,
            "headers": self._pylapi_base_headers,
        }
        # Append the auth header
        request["headers"][config_default_api_auth_header_name] = \
            (self._pylapi_auth_type + " " if self._pylapi_auth_type else "") + \
            self._pylapi_auth

        # Query params
        if query:
            request["params"] = query

        # Json payload data
        logger.debug(f"_obtain_request_args: data={data}")
        if data != None:
            # Substitute with elements in self._resource_data
            data = self._rewrite_data(data)

            request["headers"]["content-type"] = "application/json"
            request["json"] = data  # if data != {} else self._resource_data
            logger.debug(f"_obtain_request_args: request['json']={request['json']}")

        if headers != None:
            request["headers"].update(headers)

        logger.debug(f"_obtain_request_args: request={self.wash_secrets(request)}")
        return request


    # Argument names `data` and `headers` are directly referenced in resource_method(). Do not rename them.
    def _obtain_request_function(
            self,
            method_route: str,
            http_method: Any = None,
            data: dict = None,
            headers: dict = None,
            **query: Any
        ) -> function:

        logger.debug(f"_obtain_request_function(")
        logger.debug(f"    method_route={method_route},")
        logger.debug(f"    http_method={http_method},")
        logger.debug(f"    data={data},")
        logger.debug(f"    headers={self.wash_secrets(headers)},")
        logger.debug(f"    query={query},")
        logger.debug(f")")

        request_index = len(config_requests_http)  # Out of range unless set
        _http_method = http_method
        if not _http_method:
            _http_method = HTTPMethod.GET if data == None else HTTPMethod.POST
            request_index = int(_http_method)
            logger.debug(f"HTTPMethod auto assigned: {request_index}")
        elif type(_http_method) == str:
            _http_method = _http_method.upper()
            try:
                request_index = int(eval(f"HTTPMethod.{_http_method}"))
            except:
                raise Exception(f"{_http_method} is not a valid HTTPMethod")
            logger.debug(f"HTTPMethod derived from string \"{http_method}\": {request_index}")
        else:
            request_index = int(_http_method)
            logger.debug(f"HTTPMethod native: {request_index}")

        try:
            request_func = config_requests_http[request_index]
        except:
            raise Exception(f"HTTPMethod {http_method} cannot be determined")

        self._request_http_method = config_requests_http_name[request_index]
        logger.debug(f"Request Method to Use: {self._request_http_method}")

        self._request = self._obtain_request_args(method_route, data=data, headers=headers, query=query)

        # Now that _request_http_method and _request are set,
        # need to nullify _response and _response_data
        self._response = None
        self._response_data = {}

        return request_func


    ############################################################
    #
    # Class methods
    #

    @classmethod
    def auth(
        cls,
        auth: str = "",
        url: str = "",
    ) -> None:
        cls._pylapi_auth = auth
        if url:
            cls._pylapi_url = url


    @classmethod
    def wash_secrets(cls, val: Any) -> Any:
        _val = val
        if _val != None:
            if cls._pylapi_auth:
                if type(val) in (dict, list):
                    _val = json.dumps(_val)
                _val = _val.replace(cls._pylapi_auth, "<api_auth>")
                if type(val) in (dict, list):
                    _val = json.loads(_val)
            else:
                if type(val) == dict:
                    _val = {"error": "<not_authed>"}
                elif type(val) == list:
                    _val = ["<not_authed>"]
        return _val


    @classmethod
    def _resource_class(cls, resource_name: str) -> PyLapi:
        # logger.debug(f"_resource_class: resource_name={resource_name}")
        # logger.debug(f"_resource_class: _pylapi_resource_classes={cls._pylapi_resource_classes}")
        # return cls._pylapi_resource_classes[resource_name] if resource_name in cls._pylapi_resource_classes else PyLapi
        if resource_name in cls._pylapi_resource_classes:
            return cls._pylapi_resource_classes[resource_name]
        else:
            raise Exception(f"Resource '{resource_name}' not found")


    @classmethod
    def resource(cls, resource_name: str, data: dict=None, **kwargs) -> PyLapi:
        # logger.debug(f"resource: resource_name={resource_name}, data={data}, kwargs={kwargs}")
        _data = data if data != None else kwargs
        return cls._resource_class(resource_name)(resource_data=_data)


    ############################################################
    #
    # Path variable indexing
    #

    def __getitem__(self, path) -> Any:
        # logger.debug(f"__getitem__: {path}")
        item = PathDict(self._resource_data)[_path_str(path)]
        if type(item) == dict:
            item = deepcopy(item)
        return item


    def __setitem__(self, path, value: Any) -> None:
        # logger.debug(f"__setitem__: {path} to {value}")
        _value = value
        if isinstance(_value, PyLapi):
            _value = _value["$"]
        elif type(_value) not in (dict, str, int, float):
            raise ValueError(f"Invalid {self._resource_name} attribute: {type(value)} {value}")
        if path == "" or path == "$" or path == "$.":
            self._resource_data = _value
        else:
            PathDict(self._resource_data)[_path_str(path)] = _value


    def __delitem__(self, path) -> None:
        # logger.debug(f"__delitem__: {type(path)} {path}")
        del PathDict(self._resource_data)[_path_str(path)]


    # def __getattr__(self, attr) -> Any:
    #     logger.debug(f"__getattr__: {type(attr)} {attr}")
    #     item = self[attr] if attr != "data" else self._resource_data
    #     return item


    def __getattr__(self, attr: str) -> Any:
        # logger.debug(f"__getattr__: {attr}")
        # logger.debug(f"self._resource_ids: {self._resource_ids}")
        if attr in self._resource_ids:
            value = self[self._resource_ids[attr]]
            # logger.debug(f"return ID value: {value}")
        else:
            # value = getattr(self, attr)
            # logger.debug(f"{super()}")
            if hasattr(super(), attr):
                value = super().__getattr__(attr)
            else:
                value = None
        return value


    def __setattr__(self, attr: str, value: Any) -> None:
        # logger.debug(f"__setattr__: {attr} to <value>")
        if attr in self._resource_ids:
            self[self._resource_ids[attr]] = value
        elif attr == "data":
            self[""] = value
        else:
            # self.__dict__[attr] = value
            super().__setattr__(attr, value)


    def __delattr__(self, attr: str) -> None:
        # logger.debug(f"__delattr__: {attr}")
        if attr in self._resource_ids:
            del self[attr]
        else:
            # del self.__dict__[attr]
            super().__delattr__(attr)


    ############################################################
    #
    # Class operations
    #

    def __str__(self) -> str:
        return json.dumps(self._resource_data, indent=config_pylapi_json_indent)


    def __repr__(self) -> str:
        return str(self)


    def __bool__(self) -> bool:
        return self._resource_data != {}


    def __len__(self) -> int:
        return len(self._resource_data)


    def __contains__(self, other) -> bool:
        return self.__getitem__(other) != None


    ############################################################
    #
    # Object property getters and setters
    #

    @property
    def allow_api_raise(self) -> dict:
        return self._allow_api_raise

    @allow_api_raise.setter
    def allow_api_raise(self, _allow_api_raise: bool):
        self._allow_api_raise = _allow_api_raise


    @property
    def resource_name(self) -> str:
        # logger.debug(f"get resource_name: {self._resource_name}")
        return self._resource_name


    @property
    def request(self):
        # logger.debug(f"get request: {type(self._request)})")
        return self.wash_secrets(self._request)


    @property
    def raw_request(self):
        # logger.debug(f"get request: {type(self._request)})")
        return self._request


    # @request.setter
    # def request(self, request: dict):
    #     logger.debug(f"set request: {self._request} <- {request}")
    #     if type(request) == dict:
    #         self._request = request
    #     else:
    #         raise ValueError(f"Invalid request: {request}")


    @property
    def request_http_method(self):
        # logger.debug(f"get request_http_method: {self._request_http_method}")
        return self._request_http_method


    @property
    def response(self):
        # logger.debug(f"get response: {self._response}")
        return self._response


    @property
    def response_data(self):
        # logger.debug(f"get response_data: {self._response_data}")
        return self._response_data


    @property
    def data(self) -> dict:
        return AttrDict(self._resource_data)


    # @classproperty
    @property
    def resource_ids(self) -> dict:
        # logger.debug(f"get resource_ids: {self._resource_ids}")
        return self._resource_ids

    @resource_ids.setter
    def resource_ids(self, _resource_ids: dict):
        # logger.debug(f"set resource_ids: {self._resource_ids} <- {_resource_ids}")
        if type(_resource_ids) == dict:
            self._resource_ids = _resource_ids
        else:
            raise ValueError(f"Invalid resource_ids: {_resource_ids}")


    # @classproperty
    @property
    def api_base_headers(self) -> dict:
        # return cls._wash_secrets(json.dumps(cls._pylapi_base_headers))
        return self.wash_secrets(self._pylapi_base_headers)

    @api_base_headers.setter
    def api_base_headers(self, _api_base_headers: dict):
        if type(_api_base_headers) == dict and _api_base_headers:
            self._pylapi_base_headers = _api_base_headers
        else:
            raise ValueError(f"Invalid api_base_headers: {_api_base_headers}")


    ############################################################
    #
    # Class property getters, setters, and deleters
    #

    # @classproperty
    # def api_auth(cls) -> str:
    #     # logger.debug(f"get api_auth")
    #     return cls.wash_secrets(cls._pylapi_auth)

    # @api_auth.setter
    # def api_auth(cls, _api_auth: str):
    #     logger.debug(f"set api_auth")
    #     if type(_api_auth) == str:
    #         # cls._pylapi_auth = _api_auth
    #         cls.auth(_api_auth)
    #     else:
    #         raise ValueError(f"Invalid api_auth")


    @classproperty
    def api_url(cls) -> str:
        # logger.debug(f"get api_url: {cls._pylapi_url}")
        return cls._pylapi_url

    @api_url.setter
    def api_url(cls, _api_url: str):
        # logger.debug(f"set api_url: {cls._pylapi_url} -> {_api_url}")
        if type(_api_url) == str and _api_url:
            cls._pylapi_url = _api_url
        else:
            raise ValueError(f"Invalid api_url: {_api_url}")


    @classproperty
    def api_auth_header_name(cls) -> str:
        return cls._pylapi_auth_header_name

    @api_auth_header_name.setter
    def api_auth_header_name(cls, _api_auth_header_name: str):
        if type(_api_auth_header_name) == str and _api_auth_header_name:
            cls._pylapi_auth_header_name = _api_auth_header_name
        else:
            raise ValueError(f"Invalid api_auth_header_name: {_api_auth_header_name}")


    @classproperty
    def api_auth_type(cls) -> str:
        return cls._pylapi_auth_type

    @api_auth_type.setter
    def api_auth_type(cls, _api_auth_type: str):
        if type(_api_auth_type) == str and _api_auth_type:
            cls._pylapi_auth_type = _api_auth_type
        else:
            raise ValueError(f"Invalid api_auth_type: {_api_auth_type}")


    ############################################################
    #
    # Helpers methods
    #

    @classmethod
    def getLogger(cls) -> str:
        return logger


    @classmethod
    def getLogLevel(cls) -> str:
        return cls._pylapi_log_level


    @classmethod
    def setLogLevel(cls, log_level=None):
        if log_level != None:
            cls._pylapi_log_level = log_level
        logger.setLevel(cls._pylapi_log_level)


    @classmethod
    def getDeepLogLevel(cls) -> str:
        return cls._pylapi_deep_log_level


    @classmethod
    def setDeepLogLevel(cls, deep_log_level=None):
        if deep_log_level != None:
            cls._pylapi_deep_log_level = deep_log_level
        logger.setLevel(cls._pylapi_deep_log_level)


    # No content check. Child classes can provide their own check
    def response_ok(self):
        logger.debug(f"Response status: {self._response.status_code}")
        return self._response.ok
        # _ok = False
        # if self._response:
        #     _status = self._response.status_code
        #     _ok = (_status >= 200 and _status <= 299)
        # return _ok


    ############################################################
    #
    # Decorators for subclasses
    #

    @classmethod
    def resource_class(cls, resource_name, resource_base_route="", **kwargs):
        logger.debug(f"resource_class(")
        logger.debug(f"    cls={cls},")
        logger.debug(f"    resource_name={resource_name},")
        logger.debug(f"    resource_base_route={resource_base_route},")
        logger.debug(f"    kwargs={kwargs}")
        logger.debug(f")")
        # @functools.wraps(cls)
        def class_wrapper(resource_cls):
            logger.debug(f"class_wrapper({resource_cls})")

            # Register with parent
            cls._pylapi_resource_classes[resource_name] = resource_cls
            logger.debug(f"_pylapi_classes={cls._pylapi_resource_classes}")
            cls._pylapi_resource_base_routes[resource_name] = resource_base_route
            logger.debug(f"_pylapi_routes={cls._pylapi_resource_base_routes}")

            # Defaults
            cls._pylapi_url = config_default_api_url
            cls._pylapi_auth_header_name = config_default_api_auth_header_name
            cls._pylapi_auth_type = config_default_api_auth_type
            cls._pylapi_base_headers = config_default_api_base_headers

            # Register with itself
            resource_cls._resource_name = resource_name
            logger.debug(f"resource_cls._resource_name={resource_cls._resource_name}")
            resource_cls._resource_ids = kwargs
            logger.debug(f"_resource_ids={resource_cls._resource_ids}")

            @functools.wraps(resource_cls)
            def init_wrapper(*args, **kwargs):
                logger.debug(f"init_wrapper({args}, {kwargs})")
                resource_obj = resource_cls.__init__(*args, **kwargs)
                return resource_obj

            return init_wrapper

        return class_wrapper


    @classmethod
    def resource_method(cls, method_route: str="", http_method: Any=None, give="", load=None, send=None):
        logger.debug(f"resource_method(")
        logger.debug(f"    cls={cls},")
        logger.debug(f"    method=route={method_route},")
        logger.debug(f"    http_method={http_method},")
        logger.debug(f"    give={give},")
        logger.debug(f"    load={load},")
        logger.debug(f"    send={send},")
        logger.debug(f")")
        def method_deco(method):
            @functools.wraps(method)
            def method_wrapper(self, *args, **kwargs):
                logger.debug(f"method={method.__qualname__} {method}")
                logger.debug(f"method_wrapper(")
                logger.debug(f"    self=<self>,")
                logger.debug(f"    args={args} {type(args)},")
                logger.debug(f"    kwargs={kwargs} {type(kwargs)},")
                logger.debug(f")")

                # Method arg names - those passed into the method
                method_inspected = inspect.getfullargspec(method)
                logger.debug(f"method_inspected={method_inspected}")

                ##########
                #
                # Determine arg_values:
                # - Fill last set of arg_values with arg_defaults
                # - Fill arg_values with arg_name:arg
                # - Reorder arg_values in the same order as arg_names
                #   - For missing args
                #     - Use kwargs if found, then remove
                #     - Use res_ids if found, but don't remove
                #     - Use None (as a place holder)
                # - Remove both implicitly and explicitly defined _res_ids
                # - More args than in arg_names
                #   - For each additional arg, use res_ids in order
                #     - If res_ids run out, the remaining args will be ignored
                # - kwargs override and remove from kwargs if used (to avoid excessive query)

                logger.debug(f"---------- {method.__qualname__}: arg_values processing")

                # Internal variables
                _kwargs = kwargs.copy()
                logger.debug(f"_kwargs={_kwargs} (initially)")
                _res_ids = self._resource_ids.copy()
                logger.debug(f"_res_ids={_res_ids} (initially)")

                arg_values = {}
                arg_names = method_inspected.args
                del arg_names[0]  # Selfless
                logger.debug(f"arg_names={arg_names}")
                logger.debug(f"{len(arg_names)} positional args in def (arg_names)")

                arg_defaults = method_inspected.defaults if method_inspected.defaults else {}
                logger.debug(f"Last {len(arg_defaults)} has defaults: {arg_defaults}")

                # Fill last set of arg_values with arg_defaults
                arg_defaults_start = len(arg_names) - len(arg_defaults)
                for ii in range(arg_defaults_start, len(arg_names)):
                    logger.debug(f"arg_names[{ii}]={arg_names[ii]}; arg_defaults[{ii - arg_defaults_start}]={arg_defaults[ii - arg_defaults_start]}")
                    arg_values[arg_names[ii]] = arg_defaults[ii - arg_defaults_start]
                logger.debug(f"arg_values={arg_values} (with defaults from def)")

                # Fill arg_values with arg_name:arg
                logger.debug("--- Fill arg_values with arg_name:arg")
                for ii in range(min(len(arg_names), len(args))):
                    arg_values[arg_names[ii]] = args[ii]
                logger.debug(f"arg_values={arg_values} (with args in call)")

                # Reorder arg_values in the same order as arg_names
                logger.debug("--- Reorder arg_values in the same order as arg_names")
                # After that, len(arg_values) == len(arg_names)
                _arg_values = {}
                # Each iteration must create _arg_values[arg_name] somehow
                # So len(arg_names) == len(_arg_values) after the loop
                # This will handle more arg_names than args
                for arg_name in arg_names:
                    if arg_name in arg_values:
                        # arg exists
                        logger.debug(f"{arg_name} in arg_values")
                        _arg_values[arg_name] = arg_values[arg_name]
                    else:
                        logger.debug(f"{arg_name} not in arg_values")
                        # Missing args
                        if arg_name in _kwargs:
                            # Use kwarg, then remove
                            logger.debug(f"  but in _kwargs[{arg_name}]={_kwargs[arg_name]}")
                            _arg_values[arg_name] = _kwargs[arg_name]
                            del _kwargs[arg_name]  # To remove from query
                        elif arg_name in _res_ids:
                            # Use _res_ids, but don't remove (leave later)
                            logger.debug(f"  but in _res_ids[{arg_name}]={_res_ids[arg_name]}->{self[_res_ids[arg_name]]}")
                            _arg_values[arg_name] = self[_res_ids[arg_name]]
                        else:
                            # Use None
                            logger.debug(f"  and None found")
                            _arg_values[arg_name] = None
                logger.debug(f"_arg_values={_arg_values} (in the order in call)")
                logger.debug(f"_kwargs={_kwargs} (after filling missing)")

                # Remove both implicitly and explicitly defined _res_ids
                logger.debug("--- Remove both implicitly and explicitly defined _res_ids")
                for arg_name in _arg_values:
                    if arg_name in _res_ids:
                        del _res_ids[arg_name]
                logger.debug(f"_res_ids={_res_ids} (after in-arg_values trimmed)")

                # For excessive args, fill with remaining _res_ids
                _res_ids_names = list(_res_ids.keys())
                if len(arg_names) < len(args):
                    # Not to use arg_names except as a marker
                    logger.debug(f"There are {len(args) - len(arg_names)} more positional arguments in call than in def")
                    logger.debug(f"Going to assign to the {len(_res_ids_names)} remain resource IDs: {_res_ids_names}")
                    for ii in range(len(arg_names), min(len(args), len(arg_names) + len(_res_ids_names))):
                        _res_ids_name = _res_ids_names[ii - len(arg_names)]  # The above range guarantee existance
                        _arg_values[_res_ids_name] = args[ii]
                        logger.debug(f"_arg_values[{_res_ids_name}] <- {args[ii]}")
                        del _res_ids[_res_ids_name]
                    logger.debug(f"arg_values={_arg_values} (extended with resource IDs)")
                    logger.debug(f"_res_ids={_res_ids} (after excessive args trimmed)")

                # _kwargs have final say - override _arg_values if still found, then remove
                _kwargs_names = list(_kwargs.keys())
                for _kwargs_name in _kwargs_names:
                    if _kwargs_name in _arg_values:
                        _arg_values[_kwargs_name] = _kwargs[_kwargs_name]
                        del _kwargs[_kwargs_name]
                logger.debug(f"_kwargs={_kwargs} (after in-arg_values trimmed)")

                ##########
                #
                # Determine _method_route
                #
                _method_route = method_route
                # API route variable names - those found in the api route
                route_var_names = re.findall(r"{([a-zA-Z_-]([0-9a-zA-Z_-])*)}", _method_route)
                route_var_names = [_[0] for _ in route_var_names]
                logger.debug(f"route_var_names={route_var_names}")

                logger.debug(f"Finding route variables: {route_var_names}")
                for route_var_name in route_var_names:
                    route_value = None
                    # Keyword args highest precedence
                    # followed by positional args
                    # Implicit ID attributes as last resort
                    if route_var_name in _kwargs:
                        # Explicitly specified in method kwargs (keyword)
                        route_value = _kwargs[route_var_name]
                        logger.debug(f"{route_var_name} <- _kwargs[{route_var_name}]={_kwargs[route_var_name]}")
                        del _kwargs[route_var_name]
                    elif route_var_name in _arg_values:
                        # Explicitly specified in method args (positional)
                        route_value = _arg_values[route_var_name]
                        logger.debug(f"{route_var_name} <- _arg_values[{route_var_name}]={_arg_values[route_var_name]}")
                    elif route_var_name in _res_ids:
                        # Implicitly specified in ID attributes
                        # logger.debug(f"{route_var_name} is in self._resource_ids: {self._resource_ids}")
                        route_value = self[_res_ids[route_var_name]]
                        logger.debug(f"{route_var_name} <- _res_ids[{route_var_name}]={_res_ids[route_var_name]}->{self[_res_ids[route_var_name]]}")
                        _arg_values[route_var_name] = route_value  # Add for callback

                    # logger.debug(f"route_value={route_value}")
                    if route_value != None:
                        logger.debug(f"Replace route variable {route_var_name} with {route_value}")
                        _method_route = _method_route.replace("{" + route_var_name + "}", route_value)

                logger.debug(f"_kwargs={_kwargs} (after route_value trimmed)")

                logger.debug(f"_method_route={_method_route}")

                logger.debug(f"_arg_values.update(kwargs): _kwargs={_kwargs}")
                _arg_values.update(_kwargs)

                logger.debug(f"---------- {method.__qualname__}: arg_values={_arg_values}")

                # Now _kwargs contains only unassigned kwargs
                request_func = self._obtain_request_function(_method_route, http_method=http_method, **_arg_values)

                # To ensure `method()` is called only once upon its first use
                # an entry in `cls._pylapi_callbacks` prevent `method()` is checked.
                if method.__qualname__ not in cls._pylapi_callbacks:
                    # Call the function to register the callbacks
                    # To avoid argument errors, faithfully pass in
                    # what the function can accept.
                    if method_inspected.varargs:
                        if method_inspected.varkw:
                            method(self, *args, **kwargs)
                        else:
                            method(self, *args)
                    elif method_inspected.varkw:
                        method(self, **kwargs)
                    else:
                        def_args = {_: _arg_values[_] for _ in list(_arg_values.keys())[0:len(arg_names)]}
                        method(self, *def_args)
                if method.__qualname__ not in cls._pylapi_callbacks:
                    # The method does not register any callbacks,
                    # Assign a {} to stop further checking.
                    cls._pylapi_callbacks[method.__qualname__] = {}

                # Rewrite the request data with "send" first before callback (so it has final say)
                if send != None and "json" in self._request:
                    logger.debug(f"Request json to be rewritten with {send}")
                    logger.debug(f"Before: {self._request['json']}")
                    self._request["json"] = self._rewrite_data(send, self._request["json"])
                    logger.debug(f"After:  {self._request['json']}")

                # cb_arg_values = arg_values.update(kwargs)  # kwargs takes precedence

                logger.debug(f"Check request callback {method.__qualname__}.request")
                logger.debug(f"cls._pylapi_callbacks={cls._pylapi_callbacks}")

                if "request" in cls._pylapi_callbacks[method.__qualname__]:
                    logger.debug(f"Calling request")
                    cls._pylapi_callbacks[method.__qualname__]["request"](self, **_arg_values)

                self.setDeepLogLevel()
                self._response = request_func(**self._request)
                self.setLogLevel()

                self._response_data = json.loads(self._response.text)
                # Only select the give path and load path if no error

                if not self.response_ok():
                    if self._allow_api_raise:
                        raise PyLapiError(self._response_data)
                    # else skip the load and give, then let response callback to handle the error
                else:
                    logger.debug(f"self._response_data={self._response_data}")
                    # Process `load` first as `give` processing will alter `response_json`

                    # Load `load` element into the object
                    # load==None (default) means NOT to load anything
                    # load=="" means to load the whole object
                    # load=="..." means to load the path
                    if load != None:
                        logger.debug(f"load={load}")
                        self[""] = self._rewrite_data(load, self._response_data)
                        # if load == "":
                        #     self[""] = self._response_data
                        # elif load in self._response_data:
                        #     self[""] = self._response_data[load]
                        # else:
                        #     raise Exception(f"Load path {load} cannot be found in the API response: {self._response_data}")

                    # Function returns only the `give` element
                    # give==None means to return nothing
                    # give=="" means to return the whole object
                    # load=="..." means to return the path
                    if give == None:
                        self._response_data = None
                    else:
                        logger.debug(f"give={give}")
                        self._response_data = self._rewrite_data(give, self._response_data)
                        # self._response_data = self._response_data[give] if give in self._response_data else {}
                        # logger.debug(f"self._response_data={self._response_data}")

                logger.debug(f"Check response callback {method.__qualname__}.response")
                if "response" in cls._pylapi_callbacks[method.__qualname__]:
                    logger.debug(f"Calling response")
                    cls._pylapi_callbacks[method.__qualname__]["response"](self, **_arg_values)

                if self._response_data != None:
                    return self._response_data
                else:
                    return

            return method_wrapper

        # Allow @resource_method instead of requiring @resource_method("")
        if (type(method_route) == str):
            # _method_route is in the argument
            logger.debug(f"method_route arg explicitly specified: \"{method_route}\"")
            return method_deco
        else:
            # method_route is not specified, and it's in fact the method now
            logger.debug(f"method_route arg not specified, taken as {method_route}")
            _method = method_route
            method_route = ""  # Default to ""
            return method_deco(_method)


    @classmethod
    def callback(cls, cb_method):
        logger.debug(f"callback: cb_method={cb_method.__qualname__} {cb_method})")
        cb_path = re.sub(r"\.<locals>.*", "", cb_method.__qualname__)
        logger.debug(f"cb_path={cb_path}")
        cb_name = re.sub(r".*\.<locals>.", "", cb_method.__qualname__)
        logger.debug(f"cb_name={cb_name}")
        if cb_path not in cls._pylapi_callbacks:
            cls._pylapi_callbacks[cb_path] = {}
        cls._pylapi_callbacks[cb_path][cb_name] = cb_method
        # @functools.wraps(cb_method)
        # def cb_wrapper(self, *args, **kwargs):
        #     logger.debug(f"cb_wrapper: {cb_method.__qualname__}(<self>, {args}, {kwargs})")
        #     return cb_method(*args, **kwargs)
        return cb_method

# PyLapi Functions

## PyLapi

- Synopsis

  - ```python
    from pylapi import PyLapi, PyLapiError
    ```

  - Constructor
    - `def __init__(self, resource_data: dict = None, allow_api_raise=False) -> None:`
      - Initialises the resource object
      - Args
        - `resource_data`: resource data to initialise the object with
        - `allow_api_raise`: API error in the response (False - default) or raised as `PyLapiError` (True)



## Class methods

- `def resource(cls, resource_name: str="", data: dict=None, **kwargs) -> PyLapi:`
  - Create a resource object identified by the `resource_name`.
  - Args
    - `resource_name`: the resource name for which the resource object is created
    - `data`: initial resource data to load into the new resource object
  - Returns: the resource object created
- `def auth(cls, auth: str) -> None:`
  - Store the authentication credential with the API class.
  - Args
    - `auth`: credential to use for all API requests
- `def wash_secrets(cls, val: Union[str, dict, list]) -> Union[str, dict, list]:`
  - Replace the credential with `<api_auth>` if found in `val`.
  - Returns:
    - If the class contains the credential,
      - the new value of `val` after the credential being replaced
      - the same value of `val` if it does not contain the credential
    - If there is no credential in the class,
      - `"<not_authed>"` if `val` is a `str`
      - `{"error": "<not_authed>"}` if `val` is a `dict`
      - `["not_authed"]` if `val` is a `list`
- `def getLogger(cls) -> logging.RootLogger:`
  - Get the `logger` object used by the class
  - Returns: the `logger` object
  
- `def getLogLevel(cls) -> int:`
  - Get the current log level
  - Returns: the current log level
- `def setLogLevel(cls, log_level: int=None) -> None:`
  - Set the current log level

## Helper methods

- `def response_ok(self) -> bool:`
  - Test if the API responded with a success.
  - Returns: `True` if the previous API call returned a status code less than 400, or `False` if otherwise
  - Notes: A resource sub-class can provide an overriding `response_ok` property to check the response content validity.

- `def del_attr(self, attr_name: str, data: Any=None) -> Any:`
  - Recursively remove all attributes of the specified name
  - Args
    - `attr_name`: the name of the attribute to be removed
    - `data`: the data from which the attribute is removed; default to the resource data
  - Returns: a copy of `data` after all attributes of the specified name removed recursively


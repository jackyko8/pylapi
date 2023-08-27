# Configurations

import logging

config_pylapi_json_indent = 2

config_default_api_url = "https://app.example.com/api/1.0"
config_default_api_auth_header_name = "Authorization"
config_default_api_auth_type = "Bearer"
config_default_api_base_headers = {}

############################################################
#
# Controls
#

# In the order of decreasing amount of logging
config_log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}
config_log_level = logging.ERROR
config_deep_log_level = logging.ERROR


############################################################
#
# Literals
#

import requests
from enum import IntEnum

class HTTPMethod(IntEnum):
    GET = 0
    HEAD = 1
    POST = 2
    PUT = 3
    DELETE = 4
    OPTIONS = 5
    PATCH = 6

config_requests_http = [
    requests.get,
    requests.head,
    requests.post,
    requests.put,
    requests.delete,
    requests.options,
    requests.patch,
]

# For logger.debug() use only
config_requests_http_name = [
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
]
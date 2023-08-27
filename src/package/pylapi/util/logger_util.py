# Setting up logger

import json
import logging
from .config import *
from .decimal_encoder import *


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(config_log_level)


def json_dumps(js):
    return json.dumps(js, cls=DecimalEncoder)


def json_log(js, alt='{...}'):
    if js == {}:
        # Empty json logged as such regardless
        ret = '{}'
    else:
        ret = js
        try:
            ret = json_dumps(js)
        except:
            pass
        # ret = alt
        # if config_log_level == logging.DEBUG:
        #     try:
        #         ret = json.dumps(js, cls=DecimalEncoder)
        #     except:
        #         ret = js
    return ret

def str_log(str, alt='"..."'):
    if str == "":
        # Empty string logged as such regardless
        ret = '""'

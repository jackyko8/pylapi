# Error Handling

from datetime import datetime
import traceback
from .logger_util import *


def error_date_time():
    now = datetime.now()
    return now.strftime('G M T, %H hour, %M minute, %S second')


def error_handler(e):
    logger.error('Error: {}'.format(e))
    logger.error(traceback.format_exc())
    # ret = speakPrompt('Error: {}, occurred at {}.'.format(str(e), errorDateTime()))
    ret = f'Error: {str(e)}, occurred at {error_date_time()}'
    # logger.debug('Error message: '+ret)
    return ret

import sys
import json
import time
from functools import wraps
import functools
import traceback
from .config import *


def result_2_json(result):
    result_str = ''
    try:
        result_str = json.loads(result)
        return result_str
    except Exception as e:
        return result_str

def auto_handle_http_response(http_func):
    @functools.wraps(http_func)
    def wrapper(*args, **kwargs):
        try:
            status, result = http_func(*args, **kwargs)
            result_str = result_2_json(result)
            if status >= 200 and status < 300:
                # msg = {'status': status, 'msg': '%s succ, result: %s' % (http_func.__name__, result_str)}
                msg = {'status': status, 'msg': result_str}
            else:
                # msg = {'status': status, 'msg': '%s fail, result: %s' % (http_func.__name__, result_str)}
                msg = {'status': status, 'msg': result_str}
        except Exception as e:
            # msg = {'status': 500, 'msg': '%s fail, exception: %s' % (http_func.__name__, str(e))}
            msg = {'status': 500, 'msg': e}
        print(msg)
        return msg
    return wrapper


class StopRetry(Exception):
    def __repr__(self):
        return 'retry stop'

def auto_retry(max_retries: int = MAX_RETRY_TIMES,
                delay: (int, float) = 0,
                step: (int, float) = 0,
                exceptions: (BaseException, tuple, list)=BaseException,
                sleep=time.sleep,
                callback=None,
                validate=None):
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            nonlocal delay, step, max_retries
            func_ex = StopRetry
            while max_retries > 0:
                try:
                    result = func(*args, **kwargs)
                    if callable(validate) and validate(result) is False:
                        continue
                    else:
                        return result
                except exceptions as ex:
                    func_ex = ex
                    if callable(callback) and callback(ex) is True:
                        return
                finally:
                    max_retries -= 1
                    # print("try times: ", MAX_RETRY_TIMES - max_retries + 1)
                    if delay > 0 or step > 0:
                        sleep(delay)
                        delay += step
            else:
                raise func_ex
        return _wrapper
    return wrapper

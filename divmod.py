"""
In this module we use built in function: divmod

time_to_string - function for transformation time  integer to string
time_function_execution - decorator with time execute function and show it
    used printing
time_function_execution - decorator with time execute function and show
    it used  logger by logging module


"""

import time
from functools import wraps

import logging


class FormatException(Exception):
    pass


def time_to_string(time_int: int) -> str:
    """
    Time to string

    :param time_int: number of seconds

    :return:
    """

    if not isinstance(time_int, int):
        raise FormatException(
            'time_int must be integer and not {}'.format(type(time_int)))

    if time_int < 0:
        raise FormatException(
            'time_int must be bigger than 0 and given {}'.format(time_int))

    time_int, seconds = divmod(time_int, 60)
    time_int, minutes = divmod(time_int, 60)
    days, hours = divmod(time_int, 24)

    return "{}d {}h {}m {}s".format(days, hours, minutes, seconds)


def time_function_execution(f):
    """
    Decorator for
    :param f:
    :return: function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = f(*args, **kwargs)
        time_execution = int(time.time() - time_start)
        print(time_to_string(time_execution))
        return result
    return wrapper


def time_function_execution_with_logger(logger: logging, level: str='debug'):
    if hasattr(logger, level):
        action = getattr(logger, level)
    else:
        action = logger.debug

    def time_decorator(f):
        """
        Decorator for
        :param f:
        :return: function
        """
        @wraps(f)
        def wrapper(*args, **kwargs):

            time_start = time.time()
            result = f(*args, **kwargs)
            time_execution = int(time.time() - time_start)

            action(time_to_string(time_execution))
            return result
        return wrapper
    return time_decorator


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)s:%(message)s', level=logging.DEBUG)

    assert time_to_string(60 * 60 * 24 + 1) == '1d 0h 0m 1s'
    assert time_to_string(60 * 24 + 1) == '0d 0h 24m 1s'
    assert time_to_string(14 * 60 * 60 * 24 + 1) == '14d 0h 0m 1s'

    # check on Exception
    try:
        time_to_string('555')
    except FormatException:
        pass
    except Exception as e:
        raise e

    try:
        time_to_string(-5)
    except FormatException:
        pass
    except Exception as e:
        raise e

    @time_function_execution
    def test1():
        time.sleep(1)
        return True

    test1()

    @time_function_execution_with_logger(logging)
    def test2():
        time.sleep(1)
        return True


    test2()

    print('It is all right!')


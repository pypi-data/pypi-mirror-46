import os
import functools


def save_cwd(function):
    functools.wraps(function)

    def wrapper(*args, **kwargs):
        current_dir = os.getcwd()
        try:
            result = function(*args, **kwargs)
            return result
        finally:
            os.chdir(current_dir)

    return wrapper()

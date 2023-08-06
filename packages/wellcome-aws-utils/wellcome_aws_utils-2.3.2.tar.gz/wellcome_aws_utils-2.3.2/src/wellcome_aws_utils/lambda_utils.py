# -*- encoding: utf-8

import functools
import sys


def log_on_error(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            print(f'args   = {args!r}', file=sys.stderr)
            print(f'kwargs = {kwargs!r}', file=sys.stderr)
            raise

    return wrapper

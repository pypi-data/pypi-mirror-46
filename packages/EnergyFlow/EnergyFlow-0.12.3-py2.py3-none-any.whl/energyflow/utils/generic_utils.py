from __future__ import absolute_import, division, print_function

import contextlib
from functools import wraps
from itertools import repeat
from multiprocessing import Pool
import os
import sys
import time

import numpy as np

__all__ = [
    'DEFAULT_EFP_FILE', 
    'concat_specs',
    'create_pool',
    'iter_or_rep', 
    'timing', 
    'transfer'
]

# get access to the data directory of the installed package and the default efp file
EF_DATA_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
DEFAULT_EFP_FILE = os.path.join(EF_DATA_DIR, 'efps_d_le_10.npz')

# handle pickling methods in python 2
if sys.version_info[0] == 2:
    import copy_reg
    import types

    def pickle_method(method):
        func_name = method.__name__
        obj = method.__self__
        cls = obj.__class__
        return unpickle_method, (func_name, obj, cls)

    def unpickle_method(func_name, obj, cls):
        for cls in cls.mro():
            try:
                func = cls.__dict__[func_name]
            except KeyError:
                pass
            else:
                break
        return func.__get__(obj, cls)

    copy_reg.pickle(types.MethodType, pickle_method, unpickle_method)

# concatenates con. and disc. specs along axis 0, handling empty disc. specs
def concat_specs(c_specs, d_specs):
    if len(d_specs):
        return np.concatenate((c_specs, d_specs), axis=0)
    else:
        return c_specs

# handle Pool not being a context manager in Python 2
@contextlib.contextmanager
def create_pool(*args, **kwargs):
    if sys.version_info[0] == 2:
        pool = Pool(*args, **kwargs)
        yield pool
        pool.terminate()
    else:
        with Pool(*args, **kwargs) as pool:
            yield pool

# return argument if iterable else make repeat generator
def iter_or_rep(arg):
    if isinstance(arg, (tuple, list)):
        if len(arg) == 1:
            return repeat(arg[0])
        else:
            return arg
    elif isinstance(arg, repeat):
        return arg
    else:
        return repeat(arg)

# timing meta-decorator
def timing(obj, func):
    @wraps(func)
    def decorated(*args, **kwargs):
        ts = time.process_time()
        r = func(*args, **kwargs)
        te = time.process_time()
        obj.times.append(te - ts)
        return r
    return decorated

# transfers attrs from obj2 (dict or object) to obj1
def transfer(obj1, obj2, attrs):
    if isinstance(obj2, dict):
        for attr in attrs:
            setattr(obj1, attr, obj2[attr])
    else:
        for attr in attrs:
            setattr(obj1, attr, getattr(obj2, attr))

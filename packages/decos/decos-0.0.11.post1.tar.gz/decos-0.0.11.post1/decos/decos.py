import functools
import time,os,sys,pdb

__all__ = ["timer","debug","safe_run"]

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


def safe_run(_func=None,*,dcs={}):
    """ Tries to run the function and throws the given error(argument)
    dcs['tb']: String to print in try block
    dcs['cb']: String to print in except block
    dcs['dv']: default value to return: default is None
    """
#     tb = tb;dv = dv; cb=cb;fb=fb
    def saferun(func):
        @functools.wraps(func)
        def try_run_function(*args,**kwargs):
#             pdb.set_trace()
            tb = f"Running the function {func.__name__}" if dcs.get('tb',None) is None else dcs.get('tb')
            cb = f"Something wrong happened while running {func.__name__} --" if dcs.get('cb',None) is None else dcs.get('cb')
            try:
                print(tb)
                value = func(*args,**kwargs)
                return value
            except Exception as e:
                print(cb+f'{e}'+f'More info over here... \n{sys.exc_info()}')
                return dcs.get('dv',None)
#             finally:
#                 if fb:
#                     pass
#                 else:
#                     pass ## haven't decided the functionality
        return try_run_function
    if _func is None:
        return saferun
    else:
        return saferun(_func)
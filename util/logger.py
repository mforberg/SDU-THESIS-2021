import time
import functools


class Decorators:

    def time_logger(self, func):
        @functools.wraps(func)
        def time_wrapper(*args, **kwargs):
            t_time = time.perf_counter()
            value = func(*args, **kwargs)
            e_time = time.perf_counter()
            elapsed_time = e_time - t_time
            print(f"{func.__name__!r} ran in {elapsed_time:.4f} secs")
            return value
        return time_wrapper

    def info_logger(self, func):
        @functools.wraps(func)
        def info_wrapper(*args, **kwargs):
            t_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            c_time = time.ctime(end_time)
            print(f"{c_time}: {result}")
            return result
        return info_wrapper
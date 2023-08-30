import time
from typing import Callable, Any
import functools

def async_timed(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        print(f"starting {func} with args {args} {kwargs} ...")
        start = time.time()
        async def wrapped():
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"finished {func} in {total:0.2f} seconds.")
        return wrapped
    return wrapper
        

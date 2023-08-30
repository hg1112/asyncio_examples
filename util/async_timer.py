import time
from typing import Callable, Any
import functools
        
def async_timed(): 
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"starting {func} with args {args} {kwargs} ...")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"finished {func} in {total:0.2f} seconds.")
        return  wrapped
    return wrapper

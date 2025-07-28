import time
from functools import wraps
from typing import Any, Callable, Dict, Tuple


def timed_step(label: str, flat: bool = False):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[Any, Dict[str, float]]:
            t0 = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - t0
            timing = {label: duration}
            if flat and isinstance(result, tuple):
                return (*result, timing)
            else:
                return result, timing

        return wrapper

    return decorator

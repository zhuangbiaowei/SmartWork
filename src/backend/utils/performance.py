import time
from functools import wraps
from typing import Callable, Any


def monitor_performance(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Performance monitoring decorator for async functions.

    Logs execution time and helps identify slow operations.

    Args:
        func: The function to monitor

    Returns:
        Wrapped function with performance logging
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"{func.__name__} 执行时间: {execution_time:.2f}s")

        return result

    return wrapper

import asyncio
from functools import wraps

from prometheus_client import Counter, Histogram


def track_metrics(counter: Counter = None, histogram: Histogram = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = asyncio.get_event_loop().time()
            result = await func(*args, **kwargs)
            duration = asyncio.get_event_loop().time() - start
            if histogram:
                histogram.observe(duration)
            if counter:
                counter.inc()

            return result

        return wrapper

    return decorator

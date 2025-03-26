import random
import string
import pickle
import functools

from redis import asyncio as aioredis

from .environs import REDIS_URL

redis_client = aioredis.from_url(url=REDIS_URL)

def generate_verification_code(length : int = 6) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def cache(expire_time: int = 60):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs_copy = kwargs.copy()
            kwargs_copy.pop("db", None)
            key = f"{func.__name__}@{args}@{kwargs_copy}"

            value = await redis_client.get(key)

            if value:
                return pickle.loads(value)

            result = await func(*args, **kwargs)
            await redis_client.setex(key, expire_time, pickle.dumps(result))

            return result
        return wrapper
    return decorator

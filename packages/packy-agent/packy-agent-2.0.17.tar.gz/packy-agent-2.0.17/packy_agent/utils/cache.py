import cachetools


def custom_cached(cache, key=cachetools.keys.hashkey, lock=None):
    def decorator(func):
        func.cache = cache
        return cachetools.cached(cache=cache, key=key, lock=lock)(func)

    return decorator

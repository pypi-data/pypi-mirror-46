import time
import inspect
import logging
import re

from functools import wraps
from collections import OrderedDict

from coc.utils import find


log = logging.getLogger(__name__)


def validate_tag(string):
    # Legal clan tags only have these characters:
    # Numbers: 0, 2, 8, 9
    # Letters: P, Y, L, Q, G, R, J, C, U, V
    if not isinstance(string, str):
        return False

    match = re.match("(?P<tag>^\s*#?[PYLQGRJCUV0289]+\s*$)|(?P<location>\d{1,10})", string)

    if not match:
        return False
    if match.group('tag'):
        return True
    if match.group('location'):
        return True

    return False


def find_key(args, kwargs):
    if args:
        key = find(lambda x: validate_tag(x), args)
        if key:
            return key

    for k, v in kwargs.items():
        key = validate_tag(v)
        if key:
            return key

    return None


def _wrap_coroutine(result):
    async def new_coro():
        return result
    return new_coro()


def _wrap_store_coro(cache, key, coro):
    async def fctn():
        value = await coro
        cache[key] = value
        return value
    return fctn()


class LRU(OrderedDict):
    def __init__(self, max_size, ttl):
        self.max_size = max_size
        self.ttl = ttl
        super().__init__()

    def __getitem__(self, key):
        self.check_expiry()

        value = super().__getitem__(key)
        self.move_to_end(value)
        return value[1]

    def __setitem__(self, key, value):
        value = (time.monotonic(), value)
        super().__setitem__(key, value)
        self.check_expiry()
        self.check_max_size()

    def check_expiry(self):
        if not self.ttl:
            return

        current_time = time.monotonic()
        to_delete = [k for (k, (v, t)) in self.items() if current_time > (t + self.ttl)]
        for k in to_delete:
            log.debug('Removed item with key %s and TTL %s seconds from cache.', k, self.ttl)
            del self[k]

    def check_max_size(self):
        if not self.max_size:
            return

        while len(self) > self.max_size:
            oldest = next(iter(self))
            log.debug('Removed item with key %s from cache due to max size %s reached', oldest, self.max_size)
            del self[oldest]


class Cache:
    def __init__(self, max_size=128, ttl=None):
        self.cache = LRU(max_size, ttl)
        self.ttl = ttl
        self.max_size = max_size
        self.fully_populated = False

    def __call__(self, *args, **kwargs):
        self.cache.check_expiry()

    def get_cache(self):
        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = find_key(args, kwargs)
                cache = kwargs.pop('cache', False)
                fetch = kwargs.pop('fetch', True)

                if not key:
                    return func(*args, **kwargs)

                if cache:
                    data = self.get(key)
                else:
                    if fetch:
                        data = func(*args, **kwargs)
                        return _wrap_store_coro(self.cache,
                                                key, data)
                    else:
                        return None

                if not data:
                    if fetch:
                        data = func(*args, **kwargs)
                    else:
                        return None

                    if inspect.isasyncgen(data):
                        return data

                    if inspect.isawaitable(data):
                        return _wrap_store_coro(self.cache,
                                                key, data)

                    self.cache[key] = data
                    return data

                else:
                    log.debug('Using cached object with KEY: %s and VALUE: %s', key, data)
                    if inspect.iscoroutinefunction(func):
                        return _wrap_coroutine(data)

                    return data

            return wrapper
        return deco

    def get(self, key):
        self.cache.check_expiry()
        o = self.cache.get(key)
        if not o:
            return None
        return o[1]

    def add(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache = LRU(self.max_size, self.ttl)

    def get_all_values(self):
        self.cache.check_expiry()
        return list(n[1] for n in self.cache.values())

    def get_limit(self, limit: int=None):
        self.cache.check_expiry()
        if not limit:
            return self.get_all_values()

        return self.get_all_values()[:limit]


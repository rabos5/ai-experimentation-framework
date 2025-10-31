from cachetools import TTLCache
from threading import Lock
from typing import Optional


def get_cache(*, max_size: int = 1, ttl: int = 40000):
    cache_state = {
        'cache': TTLCache(maxsize=max_size, ttl=ttl),
        'lock': Lock(),
    }
    
    def get(key: str):
        with cache_state['lock']:
            try:
                return cache_state['cache'][key]
            except KeyError:
                return None
    
    def set(key: str, value, ttl_override: Optional[int] = None):
        with cache_state['lock']:
            try:
                if ttl_override is not None:
                    cache_state['cache'][key] = (value, ttl_override)
                else:
                    cache_state['cache'][key] = value
                return True
            except Exception:
                return False
    
    def pop(key: str):
        with cache_state['lock']:
            try:
                cache_state['cache'].pop(key, None)
                return True
            except Exception:
                return False
    
    def get_all():
        with cache_state['lock']:
            try:
                return dict(cache_state['cache'])
            except Exception:
                return {}
    
    def get_keys():
        with cache_state['lock']:
            try:
                return list(cache_state['cache'].keys())
            except Exception:
                return []
    
    def get_values():
        with cache_state['lock']:
            try:
                return list(cache_state['cache'].values())
            except Exception:
                return []
    
    def pop_all():
        with cache_state['lock']:
            try:
                for key in list(cache_state['cache'].keys()):
                    cache_state['cache'].pop(key, None)
                return True
            except Exception:
                return False
    
    return {
        'get': get,
        'set': set,
        'pop': pop,
        'get_all': get_all,
        'get_keys': get_keys,
        'get_values': get_values,
        'pop_all': pop_all,
    }
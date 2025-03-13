from django.core.paginator import Paginator
from django.core.cache import cache


class CachedPaginator(Paginator):
    """
    Custom paginator that forces Django to use cached
    count instead of running COUNT(*)
    """
    def __init__(self, object_list, per_page, cache_key, **kwargs):
        super().__init__(object_list, per_page, **kwargs)
        self.cache_key = cache_key

    @property
    def count(self):
        """Return cached count instead of running COUNT(*) every request."""
        cached_count = cache.get(self.cache_key)
        if cached_count is not None:
            return cached_count
        # If cache is empty, store the count
        cached_count = self.object_list.count()
        cache.set(self.cache_key, cached_count, timeout=86400)  # 24 hours
        return cached_count

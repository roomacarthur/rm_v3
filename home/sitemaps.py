from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return ['home:home']

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return None

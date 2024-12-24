from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        # Include the homepage and other static pages (if any)
        return ['home:home']

    def location(self, item):
        # 'home' is the name of the URL pattern for your homepage
        return reverse(item)

    def lastmod(self, obj):
        # You can return a fixed date for static pages or use a dynamic value if applicable
        return None

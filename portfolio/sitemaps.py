from django.contrib.sitemaps import Sitemap
from .models import PortfolioProject
from django.urls import reverse


class PortfolioProjectSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return PortfolioProject.objects.filter(is_complete=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('portfolio:project_detail', args=[str(obj.slug)])


class PortfolioListSitemap(Sitemap):
    protocol = "https"
    
    def items(self):
        return ['portfolio']

    def location(self, item):
        return reverse(f'portfolio:{item}')

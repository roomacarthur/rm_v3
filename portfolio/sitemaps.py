from django.contrib.sitemaps import Sitemap
from .models import PortfolioProject
from django.urls import reverse

class PortfolioProjectSitemap(Sitemap):
    def items(self):
        return PortfolioProject.objects.all()  # Get all portfolio projects, or apply filtering if needed

    def lastmod(self, obj):
        return obj.updated_at  # Assuming your model has a timestamp for when it was last updated

    def location(self, obj):
        return reverse('portfolio:project_detail', args=[str(obj.slug)])  # Use the correct URL pattern name

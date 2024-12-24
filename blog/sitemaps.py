from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()  # You can filter or order this queryset as needed

    def lastmod(self, obj):
        return obj.edited  # Assuming your model has a timestamp for when it was last updated

    def location(self, obj):
        return reverse('blog:post_detail', args=[str(obj.slug)])  

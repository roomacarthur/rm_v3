from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse


class PostSitemap(Sitemap):
    protocol = "https"
    
    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.edited

    def location(self, obj):
        return reverse('blog:post_detail', args=[str(obj.slug)])  


class PostListSitemap(Sitemap):
    protocol = "https"

    def items(self):
        
        return ['post_list']

    def location(self, item):
        return reverse(f'blog:{item}')
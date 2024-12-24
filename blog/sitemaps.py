from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse

class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()  # You can filter or order this queryset as needed

    def lastmod(self, obj):
        return obj.edited  # Assuming your model has a timestamp for when it was last updated

    def location(self, obj):
        return reverse('blog:post_detail', args=[str(obj.slug)])  # Use the correct URL pattern name
        

# class CategorySitemap(Sitemap):
#     def items(self):
#         return Category.objects.all()  # Get all categories or apply a filter if needed

#     def lastmod(self, obj):
#         return obj.edited  # Assuming Category has an updated_at field

#     def location(self, obj):
#         return reverse('blog:category_detail', args=[str(obj.slug)])  # You may need to update this if you have a category detail view

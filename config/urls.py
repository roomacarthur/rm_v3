from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.conf import settings

from blog.sitemaps import PostSitemap, PostListSitemap
from portfolio.sitemaps import PortfolioProjectSitemap, PortfolioListSitemap
from home.sitemaps import StaticViewSitemap

sitemaps = {
    'home': StaticViewSitemap,
    'post_list': PostListSitemap,
    'portfolio_list': PortfolioListSitemap,
    'posts': PostSitemap,
    'portfolio_projects': PortfolioProjectSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('blog.urls')),
    path('', include('portfolio.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django-sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]

# ✅ Only add Debug Toolbar URLs if DEBUG is True
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

# Custom error handlers
def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)

def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)

# Assign custom views to handlers directly
handler404 = custom_404
handler500 = custom_500
handler403 = custom_403

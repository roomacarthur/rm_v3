from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('blog.urls')),
    path('', include('portfolio.urls')),
    path('summernote/', include('django_summernote.urls')),
]

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

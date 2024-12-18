from django.urls import path
from .views import PostListView, PostDetailView

app_name = 'blog'

urlpatterns = [
    path('blog/', PostListView.as_view(), name='post_list'),
    path('blog/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
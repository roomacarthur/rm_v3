from django.urls import path
from .views import PostListView, PostDetailView


app_name = 'blog'

urlpatterns = [
    path('notes/', PostListView.as_view(), name='post_list'),
    path('notes/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('work/', views.PortfolioListView.as_view(), name='portfolio'),
    path('work/<slug:slug>/', views.PortfolioDetailView.as_view(), name='project_detail'),
]
from django.urls import path
from .views import PortfolioTemplateView

app_name = 'portfolio'

urlpatterns = [
    path('work/', PortfolioTemplateView.as_view(), name='portfolio'),
]

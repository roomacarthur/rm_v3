from django.urls import path
from .views import PortfolioTemplateView

urlpatterns = [
    path('work/', PortfolioTemplateView.as_view(), name='portfolio'),
]

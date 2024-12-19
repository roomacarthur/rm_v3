from django.views.generic import TemplateView


# Create your views here.
class PortfolioTemplateView(TemplateView):
    template_name = 'portfolio/portfolio_list.html'

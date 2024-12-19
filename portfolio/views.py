from django.views.generic import ListView, DetailView
from .models import PortfolioProject

class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10  # Optional: Paginate the list view


class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
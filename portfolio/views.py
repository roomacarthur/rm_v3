from django.views.generic import ListView, DetailView
from .models import PortfolioProject
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse


class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10  # Optional: Paginate the list view


class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'


    def get_object(self, queryset=None):
        # Retrieve the object (PortfolioProject)
        obj = super().get_object(queryset)
        
        # Check if the project is completed
        if not obj.is_completed:
            # Option 1: Redirect to the list view
            return redirect(reverse('portfolio:portfolio'))  # Redirect to the portfolio list view

            # Option 2: Raise a 404 error if the project isn't completed
            # raise Http404("Project not found or is not completed.")
        
        return obj
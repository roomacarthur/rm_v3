from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse
from .models import PortfolioProject


class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10


class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        self.object = super().get_object()
        if not self.object.is_complete:
            return HttpResponseRedirect(reverse('portfolio:portfolio'))
        return super().get(request, *args, **kwargs)

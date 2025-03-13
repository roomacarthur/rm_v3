from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache

from .models import PortfolioProject
from .utils import CachedPaginator


class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        """
        Optimize query by preloading technologies and avoiding N+1 issues.
        """
        return PortfolioProject.objects.prefetch_related(
            "technologies").only(
            "id", "title", "slug", "short_description",
            "background_colour", "text_color",
            "feature_image", "is_complete"
        )

    def get_paginator(
            self, queryset, per_page, orphans=0, allow_empty_first_page=True
    ):
        """
        Override Django's default paginator to use
        cached count instead of COUNT(*)
        """
        return CachedPaginator(
            queryset,
            per_page,
            cache_key="portfolio_project_count",
            orphans=orphans,
            allow_empty_first_page=allow_empty_first_page
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch cached project count
        project_count = cache.get("portfolio_project_count")
        if project_count is None:
            project_count = PortfolioProject.objects.count()
            cache.set("portfolio_project_count", project_count, timeout=86400)  # 24 hours

        context["project_count"] = project_count
        return context


class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_object(self, queryset=None):
        """Ensure we only fetch the project once to avoid duplicate queries."""
        if not hasattr(self, "_project"):
            self._project = super().get_object(queryset)
        return self._project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object() 
        context["technologies"] = list(project.technologies.all())

        return context

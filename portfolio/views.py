from django.views.generic import DetailView, ListView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache
from django.core.paginator import Paginator

from .models import PortfolioProject


class CachedPaginator(Paginator):
    """Custom paginator that forces Django to use cached count instead of running COUNT(*)"""
    def __init__(self, object_list, per_page, cache_key, **kwargs):
        super().__init__(object_list, per_page, **kwargs)
        self.cache_key = cache_key

    @property
    def count(self):
        """Return cached count instead of running COUNT(*) every request."""
        cached_count = cache.get(self.cache_key)
        if cached_count is not None:
            return cached_count
        # If cache is empty, store the count
        cached_count = self.object_list.count()
        cache.set(self.cache_key, cached_count)
        return cached_count


class PortfolioListView(ListView):
    model = PortfolioProject
    template_name = "portfolio/project_list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        """Optimize query by preloading technologies and avoiding N+1 issues."""
        return PortfolioProject.objects.prefetch_related("technologies").only(
            "id", "title", "slug", "short_description", "background_colour", "text_color",
            "feature_image", "is_complete"
        )

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        """Override Django's default paginator to use cached count instead of COUNT(*)"""
        return CachedPaginator(queryset, per_page, cache_key="portfolio_project_count", orphans=orphans, allow_empty_first_page=allow_empty_first_page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ✅ Fetch cached project count
        project_count = cache.get("portfolio_project_count")
        if project_count is None:
            project_count = PortfolioProject.objects.count()
            cache.set("portfolio_project_count", project_count)

        context["project_count"] = project_count
        return context

class PortfolioDetailView(DetailView):
    model = PortfolioProject
    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_object(self, queryset=None):
        """ Fetch the project once, avoiding duplicate queries. """
        return PortfolioProject.objects.prefetch_related("technologies").get(slug=self.kwargs["slug"])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_complete:
            return HttpResponseRedirect(reverse("portfolio:portfolio"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rendered_content"] = self.object.render_markdown_content()  # ✅ Pre-render Markdown in the view
        return context

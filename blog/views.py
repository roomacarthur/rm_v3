from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.cache import cache

from .models import Post, Category
from .utils import CachedPaginator


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        """Ensure category & search filters work together properly."""
        queryset = (
            Post.objects
            .select_related("category", "author")
            .only(
                "id", "title", "slug", "feature_image", "excerpt",
                "created", "category__name", "category__background_colour",
                "category__text_color", "author__username"
            )
            .order_by("-created")
        )

        # Ensure category & search filters work together properly
        category_slug = self.request.GET.get("category")
        search_query = self.request.GET.get("search")

        if category_slug and search_query:
            queryset = queryset.filter(
                category__slug=category_slug,
                title__icontains=search_query
            )
        elif category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        elif search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset

    def get_paginator(
            self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        """
        Override Django's paginator to use cached post count instead of
        COUNT(*)
        """
        return CachedPaginator(
            queryset, per_page, cache_key="blog_post_count",
            orphans=orphans, allow_empty_first_page=allow_empty_first_page
        )

    def get_context_data(self, **kwargs):
        """Optimize context data by caching post count and categories."""
        context = super().get_context_data(**kwargs)

        # Fetch cached post count
        post_count = cache.get("blog_post_count")
        if post_count is None:
            post_count = Post.objects.count()
            cache.set("blog_post_count", post_count, timeout=86400)  # 24 hours
        context["post_count"] = post_count

        # Fetch cached categories
        categories = cache.get("blog_categories")
        if categories is None:
            categories = list(
                Category.objects.only(
                    "name", "slug", "background_colour", "text_color"
                )
            )
            cache.set("blog_categories", categories, timeout=86400)  # 24 hours
        context["categories"] = categories

        return context

    def get_template_names(self):
        """Return partial template for HTMX requests."""
        if self.request.htmx:
            return ["blog/partials/post_list_partial.html"]
        return ["blog/post_list.html"]


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self):
        """ Fetch the post once, avoiding duplicate queries. """
        if not hasattr(self, "_post"):
            self._post = Post.objects.select_related(
                "category", "author").get(slug=self.kwargs["slug"])
        return self._post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()
        context["post"] = post
        context["rendered_content"] = post.render_markdown()

        if post.hashtags:
            context["formatted_hashtags"] = [
                f"#{tag.strip().lower()}" for tag in post.hashtags.split(",")
            ]

        context["related_posts"] = (
            Post.objects
            .select_related("category")
            .only("id", "title", "slug", "created", "category__name")
            .filter(category=post.category)
            .exclude(id=post.id)[:5]
        )

        return context

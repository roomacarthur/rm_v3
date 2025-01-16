from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.db.models import Q


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all()
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('search')

        # Filter by category
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Search filter
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(hashtags__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()

        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return 'blog/partials/post_list_partial.html'
        return 'blog/post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['rendered_content'] = post.render_markdown()  # rendered MD HTML

        if post.hashtags:
            hashtags = post.hashtags.split(',')  # Split by commas
            formatted_hashtags = [f"#{tag.strip().lower()}" for tag in hashtags]  # Format hashtags
            context['formatted_hashtags'] = formatted_hashtags

        # Related posts based on category (excluding the current post)
        context['related_posts'] = Post.objects.filter(
            category=post.category
        ).exclude(id=post.id)[:5]

        return context

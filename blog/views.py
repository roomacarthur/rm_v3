from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.shortcuts import render
from .models import Post, Category

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5  # Number of posts to load per request

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_htmx'] = self.request.headers.get('HX-Request') == 'true'
        context['categories'] = Category.objects.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if context['is_htmx']:
            return render(self.request, 'blog/partials/post_list_partial.html', context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

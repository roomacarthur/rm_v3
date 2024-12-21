from django.views.generic import TemplateView
from blog.models import Post


class Home(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        # Get the base context
        context = super().get_context_data(**kwargs)
        # Add latest blog posts to the context
        context['posts'] = Post.objects.order_by('-created')[:3]
        return context

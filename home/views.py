from django.views.generic import TemplateView
from blog.models import Post

class Home(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        # Get the base context
        context = super().get_context_data(**kwargs)

        context["posts"] = (
            Post.objects
            .select_related("category")  # Fetch related category
            .only(
                "id", "title", "slug", "feature_image", "excerpt",
                "category__name", "category__background_colour", "category__text_color"
            )
            .order_by("-created")[:3]
        )
        return context

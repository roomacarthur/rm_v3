from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from colorfield.fields import ColorField
from markdown import markdown
from django.utils.safestring import mark_safe

# Models

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    background_colour = ColorField(default='000000')
    text_color = ColorField(default='ffffff')
    description = models.TextField(blank=True, help_text="Optional description of the technology.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"


class PortfolioProject(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    background_colour = ColorField(default='000000')
    text_color = ColorField(default='ffffff')
    short_description = models.CharField(max_length=255)
    content = models.TextField()  # Supports Markdown for rich content
    feature_image = CloudinaryField('project-image', null=True, blank=True)
    technologies = models.ManyToManyField(Technology, related_name="projects")
    meta_description = models.TextField(max_length=160)
    meta_keywords = models.CharField(max_length=255, help_text="Comma-separated SEO keywords")
    project_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def render_markdown_content(self):
        """Render Markdown content into HTML."""
        extensions = ['fenced_code', 'codehilite', 'tables', 'attr_list']
        return mark_safe(markdown(self.content, extensions=extensions))

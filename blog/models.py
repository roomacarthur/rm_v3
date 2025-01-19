from datetime import timezone
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from cloudinary.models import CloudinaryField
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from django.utils.safestring import mark_safe


import logging
logger = logging.getLogger(__name__)


class Category(models.Model):
    name = models.CharField(max_length=100)
    background_colour = ColorField(default='000000')
    text_color = ColorField(default='ffffff')
    slug = models.SlugField(max_length=100, unique=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_image = CloudinaryField('post-image', null=True, blank=True)
    excerpt = models.TextField(max_length=200)
    content = models.TextField()
    hashtags = models.CharField(max_length=255, help_text="Comma-separated hashtags")
    meta_description = models.TextField(max_length=160)
    meta_keywords = models.CharField(max_length=255, help_text="Comma-separated SEO keywords")
    alt_text = models.CharField(max_length=100, help_text="Alt text for feature image")
    created = models.DateTimeField()
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def render_markdown(self):
        extensions = [
            'fenced_code',  # Enables fenced code blocks
            CodeHiliteExtension(linenums=False),  # Enables Pygments highlighting
            'tables',
            'attr_list',
        ]
        # Process Markdown content
        html_content = markdown.markdown(self.content, extensions=extensions, output_format="html5")
        return mark_safe(html_content)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate slug if not provided
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_hashtags_list(self):
        """Return hashtags as a list of strings."""
        return [tag.strip() for tag in self.hashtags.split(',') if tag.strip()]

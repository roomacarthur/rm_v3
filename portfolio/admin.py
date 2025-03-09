from django.contrib import admin
from .models import Technology, PortfolioProject

# Technology Admin
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'background_colour', 'text_color')
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}

# PortfolioProject Admin
@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_complete', 'created_at', 'updated_at')
    list_filter = ('is_published', 'is_complete', 'technologies')
    search_fields = ('title', 'short_description', 'meta_keywords', 'content')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('technologies',)  # For better ManyToMany field management
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'content', 'feature_image', 'project_url', 'repo_url')
        }),
        ('Technologies', {
            'fields': ('technologies',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Appearance', {
            'fields': ('background_colour', 'text_color')
        }),
        ('Status', {
            'fields': ('is_complete', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

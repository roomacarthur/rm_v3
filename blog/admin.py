from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category


class PostAdmin(SummernoteModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'category', 'created')
    search_fields = ('title', 'meta_keywords', 'hashtags')
    list_filter = ('category', 'created')
    summernote_fields = ('content',)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)


    
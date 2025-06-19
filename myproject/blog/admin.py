from django.contrib import admin
from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "views_count", "is_published",)
    search_fields = ("is_published",)

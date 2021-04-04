from django.contrib import admin
from .models import Article
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "image",
        "date_published",
        "local_post_link",
        "post_link",
    )
    list_filter = ("date_published",)
    search_fields = ("text",)
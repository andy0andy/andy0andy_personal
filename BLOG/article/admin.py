from django.contrib import admin

from .models import ArticlePost

# Register your models here.

@admin.register(ArticlePost)
class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ['author','title','title_img','tags','body','created','updated',]

    list_filter = ['tags',]
    search_fields = ['title','body','tags',]
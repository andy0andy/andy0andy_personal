from django.contrib import admin

from .models import Comments

# Register your models here.

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user','article','body','created']

    list_filter = ['user','article']
    search_fields = ['user','article','body','created']
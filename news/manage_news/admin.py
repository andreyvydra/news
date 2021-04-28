from django.contrib import admin

# Register your models here.
from .models import News, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']

    class Meta:
        model = Tag


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_urgent', 'category', 'get_tags']
    search_fields = ['title', 'content']
    list_filter = ['tags', 'author', 'category']


admin.site.register(News, NewsAdmin)
admin.site.register(Tag, TagAdmin)

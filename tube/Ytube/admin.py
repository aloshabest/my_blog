from django.contrib import admin
from .models import Post, Group
from django.utils.safestring import mark_safe


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    list_display = ('id', 'title', 'slug', 'created_at', 'get_photo', 'views', 'group')
    list_editable = ('group',)
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'author', 'content', 'photo', 'get_photo', 'views', 'created_at', 'group')


    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'



admin.site.register(Post, PostAdmin)
admin.site.register(Group)


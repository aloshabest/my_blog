from django.contrib import admin
from .models import Post, Group, Author
from django.utils.safestring import mark_safe


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    save_as = True
    list_display = ('id', 'title', 'slug', 'created_at', 'get_photo', 'views', 'group', 'author')
    list_editable = ('group', 'author',)
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = ('title', 'slug', 'author', 'content', 'photo', 'get_photo', 'views', 'created_at', 'group')


    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'

    class Meta:
        model = Post


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Author, AuthorAdmin)


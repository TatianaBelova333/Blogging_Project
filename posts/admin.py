from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from posts.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'author_link',
        'created',
        'updated',
    )
    search_fields = ('title', 'text', 'author__username')
    list_display_links = ('id',)

    def author_link(self, obj):
        author = obj.author
        url = reverse('admin:users_user_changelist') + str(author.id)
        return format_html(f'<a href="{url}">{author}</a>')


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = (
        'id',
        'text',
        'author',
        'author_link',
        'created',
        'updated',
    )
    search_fields = ('title', 'text', 'author__username')
    list_display_links = ('id',)

    def author_link(self, obj):
        author = obj.author
        url = reverse('admin:users_user_changelist') + str(author.id)
        return format_html(f'<a href="{url}">{author}</a>')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    '''
    @summary: Admin class for the `Bookmark` model.
    '''
    list_display = ['user', 'item', 'bookmarked_count', 'date_added']
    list_filter = ['date_added']

    def item(self, obj):
        return mark_safe(f'<a href="{obj.get_content_url()}">{obj.content_object}</a>')
    
    def bookmarked_count(self, obj):
        # Count of bookmarks exists for the `obj.content_object`
        return Bookmark.objects.get_bookmarks_count(obj.content_object)

    item.short_description = 'Bookmark Item'
    bookmarked_count.short_description = 'Bookmarked count'


admin.site.register(Bookmark, BookmarkAdmin)

from django.contrib import admin

from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    '''
    @summary: Admin class for the `Bookmark` model.
    '''
    list_display = ['user', 'content_object', 'date_added',]
    list_filter = ['date_added']

admin.site.register(Bookmark, BookmarkAdmin)

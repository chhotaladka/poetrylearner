from django.contrib import admin

from .models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    '''
    @summary: Admin class for the `Bookmark` model.
    '''
    list_display = ['user', 'item', 'date_added',]
    list_filter = ['date_added']

    def item(self, obj):
        return '<a href="%s">%s</a>' % (obj.get_content_url(), obj.content_object)
    
    item.short_description = 'Bookmark Item'
    item.allow_tags = True


admin.site.register(Bookmark, BookmarkAdmin)

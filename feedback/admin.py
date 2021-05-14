from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.safestring import mark_safe

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    '''
    @summary: Admin class for the `Feedback` model.
    '''
    
    list_display = ['text_excerpt', 'user_email', 'content', 'page', 'date_added',]
    
    list_filter = ['date_added',]
    #Giving error: date_hierarchy = 'date_added'
    search_fields = ['added_by__email', 'email', 'url', 'text', ]

    def text_excerpt(self, obj):
        return truncatechars(obj.text, 80)
    
    text_excerpt.short_description = _('Text excerpt')

    def content(self, obj):
        return mark_safe(f'<a href="{obj.get_content_url()}">{truncatechars(obj.content_object, 40)}</a>')

    def page(self, obj):
        return mark_safe(f'<a href="{obj.get_page_url()}">link</a>')
    
    def user_email(self, obj):
        if obj.added_by:
            return obj.added_by.email
        return obj.email
    
    user_email.short_description = _('Email')


admin.site.register(Feedback, FeedbackAdmin)
from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _

from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    '''
    @summary: Admin class for the `Feedback` model.
    '''
    
    list_display = ['date_added', 'user_email', 'url', 'text_excerpt', ]
    
    list_filter = ['date_added', 'url', ]
    date_hierarchy = 'date_added'
    search_fields = ['added_by__email', 'email', 'url', 'text', ]

    def text_excerpt(self, obj):
        return truncatewords(obj.text, 10)
    
    text_excerpt.short_description = _('Text excerpt')

    def user_email(self, obj):
        if obj.added_by:
            return obj.added_by.email
        return obj.email
    
    user_email.short_description = _('Email')


admin.site.register(Feedback, FeedbackAdmin)
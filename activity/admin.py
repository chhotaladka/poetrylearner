from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.translation import ugettext_lazy as _

from .models import Action


class ActionAdmin(admin.ModelAdmin):
    '''
    @summary: Admin class for the `Action` model.
    '''
    list_display = ['actor', 'verb', 'change_message', 'timestamp',]
    list_filter = ['timestamp']

admin.site.register(Action, ActionAdmin)
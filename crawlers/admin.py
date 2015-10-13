from django.contrib import admin

# Register your models here.
from crawlers.models import RawArticle

class RawArticleAdmin(admin.ModelAdmin):
    list_display = ('source_url', 'content', 'added_at', 
                    'valid', 'snippet')
    
    fieldsets = [
        (None,               {'fields': ['source_url', 'content', 
                                         'valid', 'snippet']
                              
                              }
         ),
        
    ]
    list_filter = ['added_at']
    search_fields = ['content']
    

admin.site.register(RawArticle, RawArticleAdmin)
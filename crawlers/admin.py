from django.contrib import admin

# Register your models here.
from crawlers.models import RawArticle, RawAuthor

class RawArticleAdmin(admin.ModelAdmin):
    list_display = ('source_url', 'added_at', 
                    'valid', 'snippet')
    
    fieldsets = [
        (None,               {'fields': ['source_url', 'content', 
                                         'valid', 'snippet']
                              
                              }
         ),
        
    ]
    list_filter = ['added_at']
    search_fields = ['content']
    
class RawAuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth', 'death', 'source_url',
                    'added_at', 'valid')
    
    fieldsets = [
        (None,               {'fields': ['name', 'birth', 'death', 'source_url', 'valid', 
                                         ]
                              
                              }
         ),
        
    ]
    list_filter = ['added_at', 'valid']
    search_fields = ['name']    
    

admin.site.register(RawArticle, RawArticleAdmin)
admin.site.register(RawAuthor, RawAuthorAdmin)
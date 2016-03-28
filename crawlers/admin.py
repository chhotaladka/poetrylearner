from django.contrib import admin

# Register your models here.
from crawlers.models import RawArticle, RawAuthor

class RawArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'source_url', 'added_at', 
                    'valid',)
    
    fieldsets = [
        (None,               {'fields': ['title', 'author', 'source_url', 'content',
                                         ]
                              
                              }
         ),
        
    ]
    list_filter = ['added_at', 'valid']
    search_fields = ['title', 'author', 'content']


    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('source_url', 'content')
        return self.readonly_fields
        
    
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
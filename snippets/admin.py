from django.contrib import admin

# Register your models here.
from snippets.models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'body', 'language', 'published', 
                    'added_by', 'added_at', 
                    'updated_by', 'updated_at')
    
    fieldsets = [
        (None,               {'fields': ['title', 'author', 'body', 'language',
                                         'tags', 'published',
                                         ]
                              
                              }
         ),
        
    ]
    list_filter = ['updated_at', 'published']
    search_fields = ['title', 'author', 'body', 'tags']
    
    
admin.site.register(Snippet, SnippetAdmin)
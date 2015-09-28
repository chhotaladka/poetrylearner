from django.contrib import admin

# Register your models here.
from crawlers.models import RawArticle

class RawArticleAdmin(admin.ModelAdmin):
    list_display = ('source_url', 'content', 'date_added', 
                    'is_valid', 'article')
    
    fieldsets = [
        (None,               {'fields': ['source_url', 'content', 
                                         'is_valid', 'article']
                              
                              }
         ),
        
    ]
    list_filter = ['date_added']
    search_fields = ['content']
    

admin.site.register(RawArticle, RawArticleAdmin)
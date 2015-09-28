from django.contrib import admin

# Register your models here.
from articles.models import Article
from projects.models import Book, Author
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'book', 'page_num', 'author', 
                    'added_by', 'modified_by', 'meta')
    fieldsets = [
        (None,   {'fields': ['title', 'content', 'page_num', 'book', 'author', 
                             'added_by', 'modified_by']}),
        
    ]
    #list_filter = ['date_added']
    search_fields = ['content']
       
       
admin.site.register(Article, ArticleAdmin)
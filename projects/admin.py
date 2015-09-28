from django.contrib import admin

# Register your models here.
from projects.models import Project, ImageSource, Book, Author

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('book', 'note', 'state', 'source', 'source_url', 'pages', 
                    'start_date', 'end_date',
                    'manager', 'date_modified')
    
    fieldsets = [
        (None,   {'fields': ['book', 'source', 'source_url', 'pages', 'manager']                 
                 }
         ),
        
    ]
    #list_filter = ['start_date']
    search_fields = ['book', 'note']


class ImageSourceAdmin(admin.ModelAdmin):
    list_display = ('project', 'page_num', 'url')
    
    fieldsets = [
        (None,   {'fields': ['project', 'page_num', 'url']                 
                 }
         ),
        
    ]
    list_filter = ['project']
    search_fields = ['url']
    

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sobriquet', 'date_birth', 'date_death', 
                    'image', 'summary', 'source_url', 'date_modified', 'modified_by')
    fieldsets = [
        (None,   {'fields': ['name', 'sobriquet', 'date_birth', 'date_death', 
                             'image', 'summary', 'source_url']
                }
        ),
        
    ]
    search_fields = ['name', 'summary']
    

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'publisher', 'year_published', 
                    'language', 'date_modified', 'modified_by')
    fieldsets = [
        (None,   {'fields': ['name', 'authors', 'pid', 
                             'publisher', 'year_published', 'language', 'modified_by']
                }
        ),
    ]
    search_fields = ['name', 'authors']
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(ImageSource, ImageSourceAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
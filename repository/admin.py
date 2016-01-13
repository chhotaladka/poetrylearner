from django.contrib import admin
from repository.models import *

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'same_as',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'has_map', 'address',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description', 'address']
    list_filter = ['date_added', 'date_modified']
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'manufacturer',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'isbn', 'creator', 'publisher',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description', 'isbn']
    list_filter = ['date_added', 'date_modified']
    

class PoetryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'body', 'date_published', 
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'body']
    list_filter = ['date_added', 'date_modified']
    

class SnippetAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'same_as', 'date_published', 
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'body']
    list_filter = ['date_added', 'date_modified']
    

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'body')
    
    search_fields = ['name','body']


admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Poetry, PoetryAdmin)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Reference, ReferenceAdmin)
from django.contrib import admin
from django.template.defaultfilters import truncatewords
from repository.models import *

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'same_as',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.description, 10)    
    info.short_description = 'info'
    

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'has_map', 'address',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description', 'address']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.description, 10)    
    info.short_description = 'info'    
    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'manufacturer',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.description, 10)    
    info.short_description = 'info'    
    

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'type',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.description, 10)    
    info.short_description = 'info'    
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.description, 10)    
    info.short_description = 'info'    
    

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'info', 'isbn', 'creator', 'publisher',
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'description', 'isbn']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.description, 10)    
    info.short_description = 'info'    
    

class PoetryAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'info', 'date_published', 
                    'added_by', 'date_added', 
                    'modified_by', 'date_modified')
    
    search_fields = ['name', 'body']
    list_filter = ['date_added', 'date_modified']
    
    def info(self, obj):
        return truncatewords(obj.body, 10)    
    info.short_description = 'body'    
    

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
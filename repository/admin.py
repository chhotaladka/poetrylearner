from django.contrib import admin
from repository.models import *

# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    pass

class PlaceAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class OrganizationAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    pass

class PoetryAdmin(admin.ModelAdmin):
    pass

class SnippetAdmin(admin.ModelAdmin):
    pass

class ReferenceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Poetry, PoetryAdmin)
admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Reference, ReferenceAdmin)
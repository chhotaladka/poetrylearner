from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

UserAdmin.list_display = ('first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
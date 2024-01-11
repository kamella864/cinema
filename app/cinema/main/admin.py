from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Custom fields', {'fields': ('birth_date', 'gender')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Cinema)
admin.site.register(Producer)
admin.site.register(Actor)
admin.site.register(Cast)
admin.site.register(History)
admin.site.register(Genre)

from http.client import ImproperConnectionState
from django.contrib import admin


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from the_people.models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)

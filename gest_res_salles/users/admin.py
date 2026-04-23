from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('profil', {'fields': ('role', 'telephone', 'matricule','must_change_password')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email', 'role', 'telephone', 'matricule','must_change_password'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

admin.site.register(User, CustomUserAdmin)
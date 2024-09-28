from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'mobile', 'isVerified', 'isRejected', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'mobile', 'address', 'thikana', 'gender', 'education', 'date_of_birth', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'isVerified', 'isRejected', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'mobile', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('email', 'username', 'mobile', 'full_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

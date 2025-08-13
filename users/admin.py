from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_admin'),
        }),
    )
    actions = ['make_employee', 'make_admin']

    def make_employee(self, request, queryset):
        queryset.update(is_employee=True, is_staff=True)
    make_employee.short_description = "تعيين كموظفين"

    def make_admin(self, request, queryset):
        queryset.update(is_admin=True, is_staff=True, is_superuser=True)
    make_admin.short_description = "تعيين كمسؤولين"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'phone')
    raw_id_fields = ('user',)
    list_select_related = ('user',)

admin.site.register(CustomUser, CustomUserAdmin)
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from . import views
from cars.models import Car, Booking, CarReview, Discount, Maintenance
from users.models import CustomUser, Customer

class CustomAdminSite(AdminSite):
    site_header = _("نظام إدارة تأجير السيارات")
    site_title = _("لوحة التحكم الإدارية")
    index_title = _("مرحباً في النظام")
    site_url = None

    def get_urls(self):
        urls = super().get_urls()
        # إضافة مسار لوحة التحكم
        custom_urls = [
            path('dashboard/', self.admin_view(views.admin_dashboard), name='dashboard'),
        ]
        return custom_urls + urls

# إنشاء نسخة مخصصة من لوحة التحكم مع تحديد الـ namespace
custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.app_name = 'custom_admin'  # تحديد الـ namespace

# تسجيل النماذج مع واجهة الإدارة المخصصة
@admin.register(Car, site=custom_admin_site)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'is_available', 'view_on_site')
    list_editable = ('price_per_day', 'is_available')
    
    def view_on_site(self, obj):
        url = reverse('car_detail', kwargs={'car_id': obj.id})
        return format_html('<a class="button" href="{}" target="_blank">معاينة في الموقع</a>', url)

@admin.register(CustomUser, site=custom_admin_site)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_admin', 'is_active')
    list_filter = ('is_staff', 'is_admin', 'is_active')
    search_fields = ('username', 'email')
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "تفعيل المستخدمين المحددين"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "تعطيل المستخدمين المحددين"

# تسجيل النماذج الأخرى
custom_admin_site.register(Booking, admin.ModelAdmin)
custom_admin_site.register(CarReview, admin.ModelAdmin)
custom_admin_site.register(Discount, admin.ModelAdmin)
custom_admin_site.register(Maintenance, admin.ModelAdmin)
custom_admin_site.register(Customer, admin.ModelAdmin)
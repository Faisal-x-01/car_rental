from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from cars.models import Car, Booking
from users.models import CustomUser, Customer
from django.urls import reverse
from django.utils.html import format_html


class CustomAdminSite(AdminSite):
    site_header = _("إدارة تأجير السيارات")
    site_title = _("لوحة التحكم")
    index_title = _("مرحباً في نظام الإدارة")
    site_url = None

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # تخصيص ترتيب التطبيقات
        ordered_apps = []
        app_mapping = {app['app_label']: app for app in app_list}
        
        for app_label in ['cars', 'users', 'auth']:
            if app_label in app_mapping:
                ordered_apps.append(app_mapping[app_label])
        
        return ordered_apps

custom_admin_site = CustomAdminSite(name='custom_admin')

# تسجيل النماذج مع الواجهة المخصصة
custom_admin_site.register(Car)
custom_admin_site.register(Booking)
custom_admin_site.register(CustomUser)
custom_admin_site.register(Customer)

class CarAdmin(admin.ModelAdmin):
    # ...
    def view_on_site(self, obj):
        url = reverse('car_detail', kwargs={'car_id': obj.id})
        return format_html('<a class="button" href="{}" target="_blank">معاينة في الموقع</a>', url)
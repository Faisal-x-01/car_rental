from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from admin_panel.admin import custom_admin_site  # استيراد لوحة التحكم المخصصة

urlpatterns = [
    path('admin/', include('admin_panel.urls')),  # استخدام مسارات لوحة التحكم المخصصة
    path('manager/', admin.site.urls),            # لوحة التحكم الافتراضية (اختياري)
    path('', include('cars.urls')),
    path('accounts/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
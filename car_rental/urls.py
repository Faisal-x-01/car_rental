from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('admin_panel.urls')),  # لوحة التحكم المخصصة
    path('manager/', admin.site.urls),  # واجهة الأدمن الافتراضية
    path('', include('cars.urls')),
    path('accounts/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
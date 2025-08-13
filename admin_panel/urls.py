from django.urls import path
from . import views
from .admin import custom_admin_site

urlpatterns = [
    path('', custom_admin_site.urls),  # جميع مسارات الإدارة
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
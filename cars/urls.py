from django.urls import path
from . import views
from .dashboard import AdminDashboard

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('book/<int:car_id>/', views.booking_view, name='booking_view'),
    path('booking/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('admin/dashboard/', AdminDashboard.as_view(), name='admin_dashboard'),
]
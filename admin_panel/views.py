from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from cars.models import Booking, Car, Maintenance
from django.db.models import Count, Sum

@staff_member_required
def admin_dashboard(request):
    today = timezone.now().date()
    
    # إحصائيات الحجوزات
    bookings = Booking.objects.filter(start_date__month=today.month)
    monthly_revenue = bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
    recent_bookings = bookings.order_by('-created_at')[:5]
    
    # حالة السيارات
    cars_by_status = Car.objects.values('is_available').annotate(count=Count('id'))
    
    # الصيانة النشطة
    active_maintenance = Maintenance.objects.filter(
        start_date__lte=today,
        end_date__gte=today,
        is_active=True
    )
    
    return render(request, 'admin/dashboard.html', {
        'recent_bookings': recent_bookings,
        'cars_by_status': cars_by_status,
        'monthly_revenue': monthly_revenue,
        'active_maintenance': active_maintenance,
        'today': today
    })
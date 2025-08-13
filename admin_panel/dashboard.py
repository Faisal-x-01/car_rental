from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.utils import timezone
from cars.models import Booking, Car, Maintenance

class AdminDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        
        context.update({
            'recent_bookings': recent_bookings,
            'cars_by_status': cars_by_status,
            'monthly_revenue': monthly_revenue,
            'active_maintenance': active_maintenance,
            'today': today
        })
        return context
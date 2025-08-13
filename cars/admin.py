from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .models import Car, Booking, CarReview, Discount, Maintenance
from django.utils import timezone

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'model', 'year', 'price_per_day', 'is_available', 'image_preview')
    list_filter = ('brand', 'year', 'is_available', 'fuel_type', 'transmission')
    search_fields = ('brand', 'name', 'model')
    list_editable = ('price_per_day', 'is_available')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    date_hierarchy = 'created_at'
    actions = ['make_available', 'make_unavailable']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return _("لا توجد صورة")
    image_preview.short_description = _('معاينة الصورة')
    
    def view_on_site(self, obj):
        return reverse('car_detail', kwargs={'car_id': obj.id})
    
    def make_available(self, request, queryset):
        queryset.update(is_available=True)
    make_available.short_description = _("تفعيل الحجز للسيارات المحددة")
    
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    make_unavailable.short_description = _("تعطيل الحجز للسيارات المحددة")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'start_date', 'car__brand')
    search_fields = ('user__username', 'car__brand')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    list_editable = ('status',)
    date_hierarchy = 'start_date'
    list_select_related = ('user', 'car')

@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating_stars', 'created_at')
    list_filter = ('rating', 'car__brand')
    search_fields = ('car__brand', 'user__username')
    readonly_fields = ('created_at',)
    
    def rating_stars(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    rating_stars.short_description = _('التقييم')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('car', 'percentage', 'active', 'days_left', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('car__brand', 'code')
    
    def active(self, obj):
        return obj.start_date <= timezone.now().date() <= obj.end_date
    active.boolean = True
    active.short_description = _('نشط')
    
    def days_left(self, obj):
        delta = obj.end_date - timezone.now().date()
        return max(0, delta.days)
    days_left.short_description = _('الأيام المتبقية')

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('car', 'type', 'cost', 'duration', 'is_active', 'start_date')
    list_filter = ('type', 'is_active')
    search_fields = ('car__brand', 'notes')
    list_editable = ('is_active',)
    
    def duration(self, obj):
        return f"{(obj.end_date - obj.start_date).days} {_('يوم')}"
    duration.short_description = _('المدة')
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Car, Booking

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'is_available', 'image_preview')
    list_filter = ('brand', 'year', 'is_available', 'fuel_type', 'transmission')
    search_fields = ('brand', 'model')
    list_editable = ('price_per_day', 'is_available')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        ('معلومات السيارة', {
            'fields': ('brand', 'model', 'year', 'description')
        }),
        ('التفاصيل الفنية', {
            'fields': ('fuel_type', 'transmission', 'seats')
        }),
        ('الحجز والتسعير', {
            'fields': ('price_per_day', 'is_available')
        }),
        ('الصورة', {
            'fields': ('image', 'image_preview')
        }),
        ('البيانات الإدارية', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" />')
        return "لا توجد صورة"
    image_preview.short_description = 'معاينة الصورة'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'start_date', 'car__brand')
    search_fields = ('user__username', 'car__brand')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    date_hierarchy = 'start_date'
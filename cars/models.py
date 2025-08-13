from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

User = get_user_model()

class Car(models.Model):
    FUEL_CHOICES = [
        ('gasoline', 'بنزين'),
        ('diesel', 'ديزل'),
        ('electric', 'كهرباء'),
        ('hybrid', 'هجين'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('automatic', 'أوتوماتيك'),
        ('manual', 'يدوي'),
    ]
    
    name = models.CharField(max_length=255, verbose_name='الاسم')
    brand = models.CharField(max_length=255, verbose_name='العلامة التجارية')
    model = models.CharField(max_length=255, verbose_name='الموديل')
    year = models.PositiveIntegerField(verbose_name='السنة')
    price_per_day = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='السعر اليومي'
    )
    image = models.ImageField(upload_to='cars/', verbose_name='الصورة', default='cars/default_car.jpg')
    description = models.TextField(blank=True, verbose_name='الوصف')
    fuel_type = models.CharField(
        max_length=20, 
        choices=FUEL_CHOICES, 
        default='gasoline',
        verbose_name='نوع الوقود'
    )
    transmission = models.CharField(
        max_length=20, 
        choices=TRANSMISSION_CHOICES, 
        default='automatic',
        verbose_name='ناقل الحركة'
    )
    seats = models.PositiveIntegerField(default=5, verbose_name='عدد المقاعد')
    is_available = models.BooleanField(default=True, verbose_name='متاح')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"{self.brand} {self.name}"

    class Meta:
        verbose_name = 'سيارة'
        verbose_name_plural = 'السيارات'
        ordering = ['-created_at']

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'تم التأكيد'),
        ('cancelled', 'ملغي'),
        ('completed', 'مكتمل'),
    ]
    
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name='السيارة'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name='المستخدم'
    )
    start_date = models.DateField(verbose_name='تاريخ البدء')
    end_date = models.DateField(verbose_name='تاريخ الانتهاء')
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='السعر الإجمالي',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='حالة الحجز'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"حجز {self.car} بواسطة {self.user}"

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date and self.car:
            delta = self.end_date - self.start_date
            self.total_price = delta.days * self.car.price_per_day
        super().save(*args, **kwargs)
        
    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return 0

    class Meta:
        verbose_name = 'حجز'
        verbose_name_plural = 'الحجوزات'
        ordering = ['-created_at']

# نماذج جديدة
class CarReview(models.Model):
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name='السيارة'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='المستخدم'
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='التقييم'
    )
    comment = models.TextField(blank=True, verbose_name='التعليق')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'تقييم سيارة'
        verbose_name_plural = 'تقييمات السيارات'
        ordering = ['-created_at']

    def __str__(self):
        return f"تقييم {self.car} بواسطة {self.user}"

class Discount(models.Model):
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE,
        verbose_name='السيارة'
    )
    percentage = models.PositiveIntegerField(verbose_name='النسبة المئوية')
    start_date = models.DateField(verbose_name='تاريخ البداية')
    end_date = models.DateField(verbose_name='تاريخ النهاية')
    code = models.CharField(max_length=20, unique=True, verbose_name='كود الخصم')

    class Meta:
        verbose_name = 'خصم'
        verbose_name_plural = 'الخصومات'
        ordering = ['-start_date']

    def __str__(self):
        return f"خصم {self.percentage}% على {self.car}"

class Maintenance(models.Model):
    MAINTENANCE_TYPES = [
        ('routine', 'صيانة دورية'),
        ('repair', 'إصلاح عطل'),
        ('accident', 'حادث'),
    ]
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE,
        verbose_name='السيارة'
    )
    type = models.CharField(
        max_length=50, 
        choices=MAINTENANCE_TYPES,
        verbose_name='نوع الصيانة'
    )
    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='التكلفة'
    )
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    start_date = models.DateField(verbose_name='تاريخ البدء')
    end_date = models.DateField(verbose_name='تاريخ الانتهاء')
    is_active = models.BooleanField(default=True, verbose_name='نشط؟')

    class Meta:
        verbose_name = 'صيانة'
        verbose_name_plural = 'صيانة السيارات'
        ordering = ['-start_date']

    def __str__(self):
        return f"صيانة {self.car} ({self.get_type_display()})"
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(
        _('مسؤول'),
        default=False,
        help_text=_('يميز المستخدمين الذين لديهم صلاحيات إدارية')
    )
    is_employee = models.BooleanField(
        _('موظف'),
        default=False,
        help_text=_('يميز المستخدمين الذين هم موظفين في الشركة')
    )
    
    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمين')
        ordering = ['-date_joined']

class Customer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('مستخدم')
    )
    phone = models.CharField(
        _('الهاتف'),
        max_length=20,
        blank=True,
        null=True
    )
    address = models.TextField(
        _('العنوان'),
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('تاريخ الإنشاء'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('تاريخ التحديث'),
        auto_now=True
    )
    
    class Meta:
        verbose_name = _('عميل')
        verbose_name_plural = _('العملاء')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.user.username
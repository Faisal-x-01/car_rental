from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Car, Booking
from .forms import BookingForm

def car_list(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'cars/car_list.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'cars/car_detail.html', {'car': car})

@login_required
def booking_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # التحقق من أن تاريخ الانتهاء بعد تاريخ البدء
            if start_date >= end_date:
                messages.error(request, 'تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء')
                form.add_error('end_date', 'تاريخ الانتهاء يجب أن يكون بعد تاريخ البدء')
                return render(request, 'cars/booking_form.html', {'car': car, 'form': form})
            
            # التحقق من عدم وجود حجوزات متضاربة
            conflicting_bookings = Booking.objects.filter(
                car=car,
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if conflicting_bookings.exists():
                conflict_msg = f"السيارة محجوزة من {conflicting_bookings[0].start_date} إلى {conflicting_bookings[0].end_date}"
                messages.error(request, conflict_msg)
                form.add_error(None, conflict_msg)
                return render(request, 'cars/booking_form.html', {'car': car, 'form': form})
            
            # إنشاء الحجز
            try:
                booking = form.save(commit=False)
                booking.car = car
                booking.user = request.user
                
                # حساب السعر الإجمالي
                delta = end_date - start_date
                booking.total_price = delta.days * car.price_per_day
                
                booking.save()
                messages.success(request, 'تم الحجز بنجاح!')
                return redirect('booking_confirmation', booking_id=booking.id)
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء الحجز: {str(e)}')
                return render(request, 'cars/booking_form.html', {'car': car, 'form': form})
        else:
            # إصلاح: عرض أخطاء النموذج بشكل صحيح
            for field, errors in form.errors.items():
                for error in errors:
                    # الحصول على اسم الحقل المعروض (label) إذا وجد
                    field_name = form.fields[field].label if field in form.fields else field
                    messages.error(request, f'{field_name}: {error}')
    else:
        # تعيين تواريخ افتراضية: البدء غدًا، الانتهاء بعد 3 أيام
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        three_days_later = tomorrow + timezone.timedelta(days=3)
        
        form = BookingForm(initial={
            'start_date': tomorrow,
            'end_date': three_days_later
        })
    
    return render(request, 'cars/booking_form.html', {
        'car': car,
        'form': form
    })

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'cars/booking_confirmation.html', {'booking': booking})

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'cars/user_bookings.html', {'bookings': bookings})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        try:
            booking.delete()
            messages.success(request, 'تم حذف الحجز بنجاح')
            return redirect('user_bookings')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف الحجز: {str(e)}')
            return redirect('user_bookings')
    
    return render(request, 'cars/confirm_delete.html', {'booking': booking})
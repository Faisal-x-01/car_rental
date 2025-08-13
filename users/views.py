from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import CustomerRegistrationForm, UserProfileForm
from .models import Customer

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.save()
            Customer.objects.create(user=user)
            
            # تسجيل الدخول تلقائياً بعد التسجيل
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(request, 'تم إنشاء حسابك بنجاح!')
                # توجيه المستخدم إلى الصفحة التي كان يحاول الوصول إليها
                next_url = request.GET.get('next', 'car_list')
                return redirect(next_url)
            else:
                messages.error(request, 'حدث خطأ في تسجيل الدخول التلقائي')
        else:
            messages.error(request, 'حدث خطأ في إنشاء الحساب')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    # إنشاء رابط تغيير كلمة المرور
    password_change_url = reverse_lazy('password_change')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {
        'form': form,
        'password_change_url': password_change_url
    })
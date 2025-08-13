car_rental/
├── car_rental/               # مجلد المشروع الرئيسي
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py               # مسارات المشروع الرئيسية
│   └── wsgi.py
│
├── cars/                     # تطبيق السيارات
│   ├── migrations/
│   ├── templates/
│   │   └── cars/
│   │       ├── booking_confirmation.html    # تأكيد الحجز
│   │       ├── booking_form.html            # نموذج الحجز
│   │       ├── car_detail.html              # تفاصيل السيارة
│   │       ├── car_list.html                # قائمة السيارات
│   │       ├── confirm_delete.html          # تأكيد حذف الحجز
│   │       └── user_bookings.html           # حجوزات المستخدم
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py               # مسارات التطبيق
│   └── views.py
│
├── users/                    # تطبيق المستخدمين
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   │       ├── login.html                # تسجيل الدخول
│   │       ├── password_change.html      # تغيير كلمة المرور
│   │       ├── password_change_done.html # تأكيد تغيير كلمة المرور
│   │       ├── profile.html              # الملف الشخصي
│   │       └── register.html             # تسجيل مستخدم جديد
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py               # مسارات التطبيق
│   └── views.py
│
├── admin_panel/              # تطبيق لوحة التحكم الإدارية
│   ├── templates/
│   │   └── admin/
│   │       └── base_site.html   # تخصيص واجهة الإدارة
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   └── urls.py
│
├── templates/                # القوالب العامة للمشروع
│   └── base.html             # القالب الأساسي
│
├── static/                   # الملفات الثابتة
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── car-bg.jpg
│       └── logo.png
│
├── media/                    # الملفات التي يرفعها المستخدمون
│   └── cars/
│
├── manage.py
└── requirements.txt

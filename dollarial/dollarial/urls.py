from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seleniumtest/', include('seleniumtest.urls')),
    path('account/', include('user_management.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('', include('website.urls')),
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from concerts.custom_admin import philharmony_admin

urlpatterns = [
    # Наша красивая админ-панель
    path('admin/', philharmony_admin.urls),
    
    # Стандартная админка (на всякий случай)
    path('standard-admin/', admin.site.urls),
    
    # Основное приложение
    path('', include('concerts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
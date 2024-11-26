from django.contrib import admin
from django.urls import path, include
from baseapp import views
from veterinaria import settings
from django.conf.urls.static import static

app_name = 'control'
urlpatterns = [
    path('', views.paginaweb, name='paginaweb'),
    path('recomendaciones', views.recomendaciones, name='recomendaciones'),
    path('menuprincipal', views.home, name='home'),
    path('accounts/', include('authenticaction.urls')),  # Incluye las URLs de autenticación de la aplicación modular
    path('ubicaciones/', include('baseapp.urls')),  # Incluye las URLs de autenticación de la aplicación modular
    path('sistema/', include('system.urls')),  # Incluye las URLs de autenticación de la aplicación modular
    path('administrativo/', include('administrativo.urls')),  # Incluye las URLs de autenticación de la aplicación modular
    path('veterinario/', include('veterinario.urls')),  # Incluye las URLs de autenticación de la aplicación modular
    path('admin_2023_erp/', admin.site.urls),

    # ...
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

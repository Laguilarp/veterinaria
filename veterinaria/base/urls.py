from base.views import inicio_sesion, cierre_sesion
from django.urls import path
urlpatterns = [
    path(r'login/', inicio_sesion, name='inicio_sesion'),
    path(r'logout/', cierre_sesion, name='cierre_sesion'),
]
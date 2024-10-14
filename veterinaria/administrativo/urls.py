from administrativo.views import menuprincipal
from django.urls import path
urlpatterns = [
    path(r'', menuprincipal, name='menuprincipal'),
]
from administrativo.views import menuprincipal
from administrativo.view_personas import *
from django.urls import path
urlpatterns = [
    path(r'', menuprincipal, name='menuprincipal'),
    path(r'personas/', listar_personas, name='listar_personas'),
    path('personas/add', crear_persona, name='crear_persona'),
    path('personas/eliminar/<int:pk>/', eliminar_persona, name='eliminar_persona'),
    path('personas/editar/<int:pk>/', editar_persona, name='editar_persona'),
    path('personas/activar_desactivar_perfil/', activar_desactivar_perfil, name='activar_desactivar_perfil'),
    path('personas/resetear_clave/', resetear_clave, name='resetear_clave'),
]
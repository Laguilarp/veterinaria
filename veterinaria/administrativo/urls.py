from django.urls import path

from administrativo import views
from administrativo.view_personas import listar_personas, crear_persona, editar_persona, eliminar_persona, activar_desactivar_perfil, \
    resetear_clave
from administrativo.organizacion import editar_organizacion
from administrativo.consultas import consultarpersonas, consultaHistorial, consultarMascota, vacunacion_data, \
    controlmedico_data, desparasitacion_data
from administrativo.view_cargo import listar_cargos, crear_cargo, editar_cargo, eliminar_cargo
from administrativo.reporte import view_reporte

app_name = 'administrativo'
urlpatterns = [
    #URLS CATEGORÍA ADMINISTRATIVO

    #CONSULTAS AUTOEJECUTABLES
    path('consultaAdministrativos/', views.consultaAdministrativos, name='consultaAdministrativos'),
    path('consultaPersonas/', views.consultaPersonas, name='consultaPersonas'),
    path('consultarMascota/', consultarMascota, name='consultarMascota'),
    path('vacunacion_data/', vacunacion_data, name='vacunacion_data'),
    path('controlmedico_data/', controlmedico_data, name='controlmedico_data'),
    path('desparasitacion_data/', desparasitacion_data, name='desparasitacion_data'),

    #CONSULTAS
    path('consultarpersonas/', consultarpersonas, name='consultarpersonas'),
    path('consultaHistorial/', consultaHistorial, name='consultaHistorial'),

    #MÓDULO ORGANIZACIÓN
    path('editar_organizacion/', editar_organizacion, name='editar_organizacion'),

    #MÓDULO PERSONAS
    path('personas/', listar_personas, name='listar_personas'),
    path('personas/add', crear_persona, name='crear_persona'),
    path('personas/eliminar/<int:pk>/', eliminar_persona, name='eliminar_persona'),
    path('personas/editar/<int:pk>/', editar_persona, name='editar_persona'),
    path('personas/activar_desactivar_perfil/', activar_desactivar_perfil, name='activar_desactivar_perfil'),
    path('personas/resetear_clave/', resetear_clave, name='resetear_clave'),

    path('reportes/', view_reporte, name='listar_reportes'),
]

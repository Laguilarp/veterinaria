from django.urls import path
from veterinario.views import listar_veterinarios
from veterinario.view_propietarios import *
from veterinario.view_raza import *
from veterinario.view_sexomascota import *
from veterinario.view_mascota import *
app_name = 'veterinario'
urlpatterns = [

    #MÓDULO VETERINARIOS
    path('veterinarios/', listar_veterinarios, name='listar_veterinarios'),

    #MÓDULO PROPIETARIOS
    path('propietarios/', listar_propietarios, name='listar_propietarios'),
    path('propietarios/add', crear_propietario, name='crear_propietario'),
    path('propietarios/eliminar/<int:pk>/', eliminar_propietario, name='eliminar_propietario'),
    path('propietarios/editar/<int:pk>/', editar_propietario, name='editar_propietario'),

    #MÓDULO RAZA
    path('razas/', listar_razas, name='listar_razas'),
    path('razas/add', crear_raza, name='crear_raza'),
    path('razas/eliminar/<int:pk>/', eliminar_raza, name='eliminar_raza'),
    path('razas/editar/<int:pk>/', editar_raza, name='editar_raza'),

    #MÓDULO SEXO MASCOTA
    path('sexomascota/', listar_sexo, name='listar_sexo'),
    path('sexomascota/add', crear_sexo, name='crear_sexo'),
    path('sexomascota/eliminar/<int:pk>/', eliminar_sexo, name='eliminar_sexo'),
    path('sexomascota/editar/<int:pk>/', editar_sexo, name='editar_sexo'),

    #MÓDULO MASCOTA
    path('mascotas/', listar_mascotas, name='listar_mascotas'),
    path('mascotas/add', crear_mascota, name='crear_mascota'),
    path('mascotas/eliminar/<int:pk>/', eliminar_mascota, name='eliminar_mascota'),
    path('mascotas/editar/<int:pk>/', editar_mascota, name='editar_mascota'),
]

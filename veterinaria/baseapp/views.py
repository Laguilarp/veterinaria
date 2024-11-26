import datetime
from datetime import datetime, date
from validadores import validador
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from baseapp.models import Persona
from administrativo.models import PersonaPerfil
from administrativo.chatbot import consultar_consejos
from django.contrib.auth.models import User

@login_required # Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista
def home(request):
    #DECLARACIÓN DE VARIABLES
    empleados_sin_jornadas = False
    fecha_actual = datetime.now().date()

    is_administrativo = False

    usuario = request.user
    if usuario.id:
        persona = Persona.objects.filter(status=True, usuario=usuario)
        if persona.exists():
            persona = persona.first()
            perfil = PersonaPerfil.objects.filter(status=True, persona=persona)
            if perfil.exists():
                perfil = perfil.first()
                if perfil.is_administrador:
                    is_administrativo = True

    # Luego, puedes pasar datos a tu template si es necesario
    context = {
        'page_titulo': 'Inicio',
        'titulo':'Inicio',
        'g_fechaactual': fecha_actual,
        'is_administrativo':is_administrativo,
    }

    # Renderiza el template y pasa el contexto
    return render(request, 'home.html', context)

def paginaweb(request):
    return render(request, 'paginaweb/inicio.html')

def recomendaciones(request):
    data = {}
    peticion = 'Consejos y sugerencias para el cuidado de mis mascotas'
    data['primerconsejo'] = consultar_consejos(peticion)
    data['segundoconsejo'] = consultar_consejos(peticion)
    data['tercerconsejo'] = consultar_consejos(peticion)
    return render(request, 'paginaweb/recomendaciones.html', data)
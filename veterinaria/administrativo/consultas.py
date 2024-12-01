from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from authenticaction.models import CustomUser
from baseapp.models import Persona
from veterinario.models import *


@login_required

def consultarpersonas(request):
    try:
        # Obtiene el término de búsqueda desde la solicitud GET
        search_term = request.GET.get('q', '').strip()
        resultados = Persona.objects.filter(status=True)

        # Realiza la búsqueda en la base de datos (este es un ejemplo simple, adapta según tu modelo)
        ss = search_term.split(' ')
        if len(ss) == 1:
            resultados = resultados.filter(Q(nombres__icontains=search_term) |
                                                       Q(apellido1__icontains=search_term) |
                                                       Q(apellido2__icontains=search_term) |
                                                       Q(cedula__icontains=search_term) |
                                                       Q(pasaporte__icontains=search_term))
        else:
            resultados = resultados.filter(Q(nombres__icontains=search_term) |
                                           (Q(apellido1__icontains=ss[0]) | Q(_apellido2__icontains=ss[1])))

        # Obtén los nombres de las personas como lista
        resultados = [{'id': persona.id, 'nombre': persona.__str__(), 'cedula': persona.get_card_id()} for persona in resultados[:5]]

        # Devuelve los resultados en formato JSON
        return JsonResponse(resultados, safe=False)
    except Exception as ex:
        return JsonResponse([], safe=False)

def consultaHistorial(request):
    try:
        user_message = request.GET['respuesta']

        retorno = 'No cuenta con historial médico'

        # Llamada a la API de OpenAI para procesar la pregunta
        propietario = Propietario.objects.filter(status=True, persona__documento=user_message)
        if propietario.exists():
            propietario = propietario.first()
            mascotas = propietario.mascota.filter(status=True)
            if mascotas.exists():
                retorno = 'Sí cuenta con historial médico'

        # Obtener la respuesta generada por el modelo
        chatbot_response = retorno
        return JsonResponse({"success": True, "response": chatbot_response})
    except Exception as ex:
        return JsonResponse([], safe=False)

def consultarMascota(request):
    try:
        id = int(request.GET['id'])
        mascota = Mascota.objects.get(id=id)
        return JsonResponse({"success": True, "sexo": mascota.sexo.id, "especie": mascota.raza.especie.id, "raza": mascota.raza.id})
    except Exception as ex:
        return JsonResponse({"result": False})

from system.tool_chatbot import consulta
from django.http import JsonResponse, HttpResponseRedirect
from veterinario.models import Cita, Propietario


def consultar_citas(request):
    try:
        user_message = request.GET['respuesta']

        retorno = 'No tiene citas pendientes'

        propietario = Propietario.objects.filter(status=True, persona__documento=user_message)

        if not propietario.exists():
            return JsonResponse({"success": True, "response": u'No existe persona'})

        propietario = propietario.first()

        mascotas = propietario.mascota.filter(status=True).values_list('id', flat=True)

        # Llamada a la API de OpenAI para procesar la pregunta
        citas = Cita.objects.filter(status=True, mascota__id__in=mascotas, estado=1).order_by('id').first()

        if citas:
            retorno = f"Su próxima cita es el {citas.fecha_cita} a las {citas.hora_cita}"

        # Obtener la respuesta generada por el modelo
        chatbot_response = retorno

        return JsonResponse({"success": True, "response": chatbot_response})
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")

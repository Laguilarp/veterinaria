from system.tool_chatbot import consulta
from django.http import JsonResponse, HttpResponseRedirect
from veterinario.models import Cita


def consultar_citas(request):
    try:
        user_message = request.GET['respuesta']

        retorno = 'No tiene citas pendientes'

        # Llamada a la API de OpenAI para procesar la pregunta
        citas = Cita.objects.filter(status=True, propietario__persona__documento=user_message).order_by('id').first()

        if citas:
            retorno = f"Su próxima cita es el {citas.fecha_cita} a las {citas.hora_cita}"

        # Obtener la respuesta generada por el modelo
        chatbot_response = retorno

        return JsonResponse({"success": True, "response": chatbot_response})
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")

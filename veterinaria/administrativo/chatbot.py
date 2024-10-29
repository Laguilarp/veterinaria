from system.tool_chatbot import consulta
from django.http import JsonResponse, HttpResponseRedirect


def consultar_peticion(request):
    try:
        user_message = request.GET['respuesta']

        # Llamada a la API de OpenAI para procesar la pregunta
        retorno = consulta(user_message)

        # Obtener la respuesta generada por el modelo
        chatbot_response = retorno

        return JsonResponse({"success": True, "response": chatbot_response})
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")

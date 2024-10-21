from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from authenticaction.models import CustomUser
from baseapp.models import Persona


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
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from authenticaction.models import CustomUser
from baseapp.models import Persona
from veterinario.models import *
import calendar
import locale

# Configura la localización al español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


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

def vacunacion_data(request):
    # Filtrar las citas con motivocita = VACUNACIÓN (1)
    citas_vacunacion = Cita.objects.filter(motivocita=1)

    # Contar las citas agrupadas por mes
    from django.db.models import Count
    from django.db.models.functions import ExtractMonth
    citas_por_mes = citas_vacunacion.annotate(mes=ExtractMonth('fecha_cita')).values('mes').annotate(
        total=Count('id')).order_by('mes')

    # Formatear los datos para el gráfico
    labels = [calendar.month_name[cita['mes']] for cita in citas_por_mes]
    data = [cita['total'] for cita in citas_por_mes]

    # Retornar los datos como JSON
    return JsonResponse({
        "data": data,
        "labels": labels,
    })

def controlmedico_data(request):
    # Filtrar las citas con motivocita = CONTROL MÉDICO (3)
    citas_vacunacion = Cita.objects.filter(motivocita=3)

    # Contar las citas agrupadas por mes
    from django.db.models import Count
    from django.db.models.functions import ExtractMonth
    citas_por_mes = citas_vacunacion.annotate(mes=ExtractMonth('fecha_cita')).values('mes').annotate(
        total=Count('id')).order_by('mes')

    # Formatear los datos para el gráfico
    labels = [calendar.month_name[cita['mes']] for cita in citas_por_mes]
    data = [cita['total'] for cita in citas_por_mes]

    # Retornar los datos como JSON
    return JsonResponse({
        "data": data,
        "labels": labels,
    })

def desparasitacion_data(request):
    # Filtrar las citas con motivocita = DESPARASITACIÓN (2)
    citas_vacunacion = Cita.objects.filter(motivocita=2)

    # Contar las citas agrupadas por mes
    from django.db.models import Count
    from django.db.models.functions import ExtractMonth
    citas_por_mes = citas_vacunacion.annotate(mes=ExtractMonth('fecha_cita')).values('mes').annotate(
        total=Count('id')).order_by('mes')

    # Formatear los datos para el gráfico
    labels = [calendar.month_name[cita['mes']] for cita in citas_por_mes]
    data = [cita['total'] for cita in citas_por_mes]

    # Retornar los datos como JSON
    return JsonResponse({
        "data": data,
        "labels": labels,
    })
def consultaperros(request):
    try:
        total_mascotas = Mascota.objects.filter(
            status=True,
            raza__especie_id=2  # Filtra por especie_id=2 a través de raza
        ).count()

        return JsonResponse({'success': True, 'total': total_mascotas})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
def consultagatos(request):
    try:
        total_mascotas = Mascota.objects.filter(
            status=True,
            raza__especie_id=1  # Filtra por especie_id=2 a través de raza
        ).count()

        return JsonResponse({'success': True, 'total': total_mascotas})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
def consultaotros_especie(request):
    try:
        total_mascotas = Mascota.objects.filter(
            status=True,
            raza__especie_id=3
        ).count()

        return JsonResponse({'success': True, 'total': total_mascotas})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
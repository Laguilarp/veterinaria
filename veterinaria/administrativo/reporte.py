import os
import sys
import datetime
from datetime import datetime
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.staticfiles import finders
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from veterinaria import settings
from veterinaria.settings import ALMACENAMIENTO
from veterinaria.settings import BASE_DIR, MEDIA_ROOT
from administrativo.forms import *
from administrativo.funciones import *
from administrativo.models import *
from veterinario.models import *
from django.db.models import Q

def create_mail(user_mail, subject, template_name, context):
    template = get_template(template_name)
    content = template.render(context)

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[
            user_mail
        ],
        cc=[]
    )

    message.attach_alternative(content, 'text/html')
    return message
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    path_uri = str(BASE_DIR) + str(uri)
    result = finders.find(path_uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path




def render_pdf_view(template_paths,data):
    template_path = template_paths
    context = data
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def redimenzionar_imagen(ruta_original, ruta_a_guardar, ancho, alto):
    from PIL import Image

    # Abre la imagen que quieres redimensionar
    imagen = Image.open(ruta_original)

    # Define el nuevo tamaño deseado para la imagen
    nuevo_tamaño = (ancho, alto)  # (ancho, alto)

    # Redimensiona la imagen con el nuevo tamaño
    imagen_redimensionada = imagen.resize(nuevo_tamaño)

    # Guarda la nueva imagen redimensionada
    imagen_redimensionada.save(ruta_a_guardar)


@transaction.atomic()
def view_reporte(request):
    global ex
    data = {}
    usuario_logeado = request.user

    if request.method == 'POST':
        if 'peticion' in request.POST:
            peticion = request.POST['peticion']

            if peticion == 'citasatendidas':
                try:
                    data['citas'] = citas = Cita.objects.filter(status=True, estado=2)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Citas atendidas'
                    name = "reporte" + str(citas.count())
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/citasatendidas.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'citaspendientes':
                try:
                    data['citas'] = citas = Cita.objects.filter(status=True, estado=1)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Citas pendientes'
                    name = "reporte" + str(citas.count())
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/citaspendientes.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'citasrechazadas':
                try:
                    data['citas'] = citas = Cita.objects.filter(status=True, estado=3)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Citas rechazadas'
                    name = "reporte" + str(citas.count())
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/citasrechazadas.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'mascotasatendidas':
                try:
                    data['citas'] = citas = Cita.objects.filter(status=True, estado=2).values_list('mascota__id', flat=True)
                    data['mascotas'] = mascotas = Mascota.objects.filter(status=True, id__in=citas)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Mascotas atendidas'
                    name = "reporte" + str(citas.count())
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/mascotasatendidas.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'descargarhistorial':
                try:
                    data['mascota'] = mascota = Mascota.objects.get(id=int(request.POST['id']))
                    data['historiales'] = historial = HistorialMedico.objects.filter(status=True, mascota=mascota)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial médico'
                    name = "reporte_historial" + str(mascota.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialmedicomascota.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'descargarcarnet':
                try:
                    data['mascota'] = mascota = Mascota.objects.get(id=int(request.POST['id']))
                    data['historiales'] = historial = HistorialVacunacion.objects.filter(status=True, mascota=mascota)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial médico'
                    name = "reporte_historial" + str(mascota.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialvacunacion.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'generarhistorial':
                try:
                    data['propietario'] = propietario = Propietario.objects.filter(status=True, persona__documento=request.POST['respuesta'], persona__status=True).first()
                    if not propietario:
                        return JsonResponse({"respuesta": False, "mensaje": "Persona no se encuentra registrada en el sistema"})
                    data['mascotas'] = mascota = propietario.mascota.filter(status=True)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial médico'
                    name = "reporte_historialweb" + str(propietario.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialmedicoweb.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'descargarhistorialvacuna':
                try:
                    data['propietario'] = propietario = Propietario.objects.filter(status=True, persona__documento=request.POST['respuesta'], persona__status=True).first()
                    if not propietario:
                        return JsonResponse({"respuesta": False, "mensaje": "Persona no se encuentra registrada en el sistema"})
                    data['mascotas'] = mascota = propietario.mascota.filter(status=True)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial vacunación'
                    name = "reporte_historialvacunaweb" + str(propietario.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialvacunaweb.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'descargarhistorialdespara':
                try:
                    data['propietario'] = propietario = Propietario.objects.filter(status=True, persona__documento=request.POST['respuesta'], persona__status=True).first()
                    if not propietario:
                        return JsonResponse({"respuesta": False, "mensaje": "Persona no se encuentra registrada en el sistema"})
                    data['mascotas'] = mascota = propietario.mascota.filter(status=True)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial desparasitación'
                    name = "reporte_historialvacunaweb" + str(propietario.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialdesparasitacionweb.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'generarhistorialdespara':
                try:
                    data['mascota'] = mascota = Mascota.objects.get(id=int(request.POST['id']))
                    data['historiales'] = historial = HistorialDesparasitante.objects.filter(status=True, mascota=mascota)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial médico desparasitación'
                    name = "reporte_historialdesparasitacion" + str(mascota.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialdesparasitacion.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse(
                            {"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'generarhistorialreceta':
                try:
                    data['mascota'] = mascota = Mascota.objects.get(id=int(request.POST['id']))
                    data['historiales'] = historial = HistorialMedico.objects.filter(status=True, mascota=mascota)
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial médico'
                    name = "reporte_historial" + str(mascota.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialrecetamedica.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

            if peticion == 'recetaindividual':
                try:
                    data['historiales'] = historial = HistorialMedico.objects.filter(status=True, id=int(request.POST['id']))
                    data['mascota'] = mascota = Mascota.objects.get(id=int(request.POST['idextra']))
                    data['fechaactual'] = datetime.now().date()
                    data['tiporeporte'] = 'Historial médico'
                    name = "reporte_historial" + str(mascota.id)
                    crear_carpeta = os.path.join(os.path.join(ALMACENAMIENTO, 'media', 'reportes'))
                    try:
                        os.makedirs(crear_carpeta)
                    except Exception as ex:
                        pass
                    valida = convertir_html_a_pdf_reporte(
                        'reportes/historialrecetamedica.html',
                        {'pagesize': 'A4', 'data': data, 'MEDIA_ROOT': MEDIA_ROOT}, name + '.pdf'
                    )
                    if valida:
                        return JsonResponse({"respuesta": True, "mensaje": "Reporte generado correctamente.", "name": name + '.pdf'})
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})
                except Exception as ex:
                    return JsonResponse({"respuesta": False, "mensaje": "Error al generar el certificado."})

        return JsonResponse({"respuesta": False, "mensaje": "Acción incorrecta."})
    else:
        if 'peticion' in request.GET:
            peticion = request.GET['peticion']

        else:
            try:
                parametros = ''
                context = {
                    'page_titulo': "Reportes",
                    'titulo': "Reportes",
                    'parametros': parametros,
                }
                return render(request, 'reportes/inicio.html', context)
            except Exception as ex:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

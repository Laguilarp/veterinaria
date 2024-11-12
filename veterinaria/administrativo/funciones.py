from django.db import models
import os
from veterinaria import settings
from django.contrib.staticfiles import finders
from django.http import JsonResponse, HttpResponse
from veterinaria.settings import BASE_DIR, ALMACENAMIENTO
import datetime
from datetime import datetime
from decimal import Decimal
from django.forms import model_to_dict
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
# from io import StringIO
import io as StringIO
from xhtml2pdf import pisa
import uuid

def convertir_html_a_pdf_reporte(template_src, context_dict, filename):
    template = get_template(template_src)
    html = template.render(context_dict).encode(encoding="UTF-8")
    result = StringIO.BytesIO()
    output_folder = os.path.join(ALMACENAMIENTO, 'media', 'reportes')
    filepdf = open(output_folder + os.sep + filename, "w+b")
    links = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    pdf1 = pisa.pisaDocument(StringIO.BytesIO(html), dest=filepdf, link_callback=links)
    pisaStatus = pisa.CreatePDF(StringIO.BytesIO(html), result, link_callback=links)
    if not pdf1.err:
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
        return True
    return JsonResponse({"result": "bad", "mensaje": u"Incidencias al generar el reporte"})

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

def solo_2_decimales(valor, decimales=None):
    if valor:
        if decimales:
            if decimales > 0:
                return float(Decimal(valor if valor else 0).quantize(
                    Decimal('.' + ''.zfill(decimales - 1) + '1')) if valor else 0)
            else:
                return float(Decimal(valor if valor else 0).quantize(Decimal('0')))
    return valor if valor else 0

def quitar_caracteres(cadena):
    return cadena.replace(u'ñ', u'n').replace(u'Ñ', u'N').replace(u'Á', u'A').replace(u'á', u'a').replace(u'É',u'E').replace(u'é', u'e').replace(u'Í', u'I').replace(u'í', u'i').replace(u'Ó', u'O').replace(u'ó', u'o').replace(u'Ú',u'U').replace(u'ú', u'u')

def nuevo_nombre(nombre, original):
    nombre = quitar_caracteres(nombre).lower().replace(' ', '_')
    ext = ""
    if original.find(".") > 0:
        ext = original[original.rfind("."):]
    fecha = datetime.now().date()
    hora = datetime.now().time()
    return nombre + fecha.year.__str__() + fecha.month.__str__() + fecha.day.__str__() + hora.hour.__str__() + hora.minute.__str__() + hora.second.__str__() + ext.lower()
def conviert_html_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict).encode(encoding="UTF-8")
    result = StringIO.BytesIO()
    pisaStatus = pisa.CreatePDF(StringIO.BytesIO(html), result, link_callback=link_callback)
    if not pisaStatus.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return JsonResponse({"result": "bad", "mensaje": u"Problemas al ejecutar el reporte."})

def generar_nombre(nombre, original):
    nombre = quitar_caracteres(nombre).lower().replace(' ', '_')
    ext = ""
    if original.find(".") > 0:
        ext = original[original.rfind("."):]
    fecha = datetime.now().date()
    hora = datetime.now().time()
    return nombre + fecha.year.__str__() + fecha.month.__str__() + fecha.day.__str__() + hora.hour.__str__() + hora.minute.__str__() + hora.second.__str__() + ext.lower()

def customgetattr(object, name):
    r = getattr(object, name)
    if str(type(r)) == "<class 'method'>" or str(type(r)) == "<class 'function'>":
        return r()
    return r

def remover_caracteres_tildes_unicode(cadena):
    return cadena.replace(u'Á', u'A').replace(u'á', u'a').replace(u'É', u'E').replace(u'é', u'e').replace(u'Í',
                                                                                                          u'I').replace(
        u'í', u'i').replace(u'Ó', u'O').replace(u'ó', u'o').replace(u'Ú', u'U').replace(u'ú', u'u')

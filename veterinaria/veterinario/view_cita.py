import datetime
from datetime import datetime
from validadores import validador
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from core.utils import is_ajax
from administrativo.models import Persona, PersonaPerfil
from system.tool_email import enviar_correo
from baseapp.forms import PersonaForm
from django.contrib.auth.models import User
from veterinario.models import Propietario, Raza, Cita, DetalleCita, HistorialMedico
from veterinario.forms import RazaForm, CitaForm, DetalleCitaForm
@login_required
#@validador
def listar_citas(request,search=None):
    try:
        parametros = ''
        citas = Cita.objects.filter(status=True)
        if 'search' in request.GET:
            search_ = search = request.GET['search']
            parametros += '&search=' + search_
            search_ = search_.strip()
            ss = search_.split(' ')
            if len(ss) == 1:
                citas = citas.filter(Q(veterinario__persona__nombres__icontains=search) |
                                                   Q(veterinario__persona__apellido1__icontains=search) |
                                                   Q(veterinario__persona__apellido2__icontains=search) |
                                                   Q(mascota__nombre__icontains=search) |
                                                   Q(veterinario__persona__documento__icontains=search))
            else:
                citas = citas.filter(
                    (Q(veterinario__persona__apellido1__icontains=ss[0]) & Q(veterinario__persona__apellido2__icontains=ss[1])) |
                    (Q(veterinario__persona__nombres__icontains=ss[0]) & Q(veterinario__persona__nombres__icontains=ss[1])))

        paginator = Paginator(citas, 25)
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'page_object': page_object,
            'page_titulo': "Citas",
            'titulo': "Citas",
            'search': search,
            'parametros': parametros,
        }
        return render(request, 'cita/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")


@login_required
def crear_cita(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                fechaactual = datetime.now().date()
                form = CitaForm(request.POST, request.FILES)
                if form.is_valid():
                    existe_cita = Cita.objects.filter(status=True, fecha_cita=form.cleaned_data['fecha_cita'], hora_cita=form.cleaned_data['hora_cita'], estado=1)
                    if existe_cita.exists():
                        return JsonResponse({'success': False, 'errors': u'Ya existe una cita reservada para la fecha y hora ingresada'})
                    elif form.cleaned_data['fecha_cita'] < fechaactual:
                        return JsonResponse({'success': False, 'errors': u'No puede reservar con fecha inferior a la actual'})
                    instance = Cita(
                        mascota=form.cleaned_data['mascota'],
                        veterinario=form.cleaned_data['veterinario'],
                        fecha_cita=form.cleaned_data['fecha_cita'],
                        hora_cita=form.cleaned_data['hora_cita'],
                        motivo=form.cleaned_data['motivo'],
                    )
                    instance.save(request)
                    propietario = instance.mascota.get_propietario()
                    if propietario:
                        if propietario.persona.correo_electronico:
                            # Usar la función
                            mensaje = f"""
                            <h1>¡Hola, {propietario.__str__()}!</h1>
                            <p>Acabas de agendar una cita en <strong>Medipets</strong>.</p>
                            <p><strong>Detalles de tu cita:</strong></p>
                            <ul>
                                <li><strong>Fecha:</strong> {instance.fecha_cita}</li>
                                <li><strong>Hora:</strong> {instance.hora_cita}</li>
                                <li><strong>Mascota:</strong> {instance.mascota.__str__()}</li>
                                <li><strong>Motivo:</strong> {instance.motivo}</li>
                            </ul>
                            <p>¡Gracias por confiar en nosotros!</p>
                            """

                            enviar_correo(
                                destinatario=propietario.persona.correo_electronico,
                                asunto='Cita agendada!',
                                mensaje=mensaje,
                                archivo=''  # Opcional
                            )
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = CitaForm()
        else:
            return redirect('veterinario:listar_citas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_cita(request, pk):
    instance = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                fechaactual = datetime.now().date()
                form = CitaForm(request.POST, request.FILES)
                if form.is_valid():
                    existe_cita = Cita.objects.filter(status=True, fecha_cita=form.cleaned_data['fecha_cita'], hora_cita=form.cleaned_data['hora_cita'], estado=1).exclude(id=instance.id)
                    if existe_cita.exists():
                        return JsonResponse({'success': False, 'errors': u'Ya existe una cita reservada para la fecha y hora ingresada'})
                    elif form.cleaned_data['fecha_cita'] < fechaactual:
                        return JsonResponse({'success': False, 'errors': u'No puede reservar con fecha inferior a la actual'})
                    instance.mascota = form.cleaned_data['mascota']
                    instance.veterinario = form.cleaned_data['veterinario']
                    instance.fecha_cita = form.cleaned_data['fecha_cita']
                    instance.hora_cita = form.cleaned_data['hora_cita']
                    instance.motivo = form.cleaned_data['motivo']
                    instance.save(request)
                    propietario = instance.mascota.get_propietario()
                    if propietario:
                        if propietario.persona.correo_electronico:
                            # Usar la función
                            mensaje = f"""
                                                <h1>¡Hola, {propietario.__str__()}!</h1>
                                                <p>Tu cita se ha actualizado en <strong>Medipets</strong>.</p>
                                                <p><strong>Detalles de tu cita:</strong></p>
                                                <ul>
                                                    <li><strong>Fecha:</strong> {instance.fecha_cita}</li>
                                                    <li><strong>Hora:</strong> {instance.hora_cita}</li>
                                                    <li><strong>Mascota:</strong> {instance.mascota.__str__()}</li>
                                                    <li><strong>Motivo:</strong> {instance.motivo}</li>
                                                </ul>
                                                <p>¡Gracias por confiar en nosotros!</p>
                                                """

                            enviar_correo(
                                destinatario=propietario.persona.correo_electronico,
                                asunto='Cita agendada!',
                                mensaje=mensaje,
                                archivo=''  # Opcional
                            )
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = CitaForm(initial={'mascota': instance.mascota,
                                     'veterinario': instance.veterinario,
                                     'fecha_cita': instance.fecha_cita,
                                     'hora_cita': instance.hora_cita,
                                     'motivo': instance.motivo,
                                     })
        else:
            return redirect('veterinario:listar_citas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

def atender_cita(request, pk):
    instance = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = DetalleCitaForm(request.POST, request.FILES)
                if form.is_valid():
                    valortotal = 0
                    tratamientos = form.cleaned_data['tratamiento']
                    vacunas = form.cleaned_data['inyeccion']
                    instance_ = DetalleCita(cita=instance, observacion=form.cleaned_data['observacion'])
                    instance_.save(request)
                    newhistorial = HistorialMedico(veterinario=instance.veterinario, mascota=instance.mascota,
                                                   descripcion=form.cleaned_data['observacion'],
                                                   fecha_consulta=instance.fecha_cita)
                    newhistorial.save(request)
                    for tratamiento in tratamientos:
                        valortotal += tratamiento.precio
                        instance_.tratamiento.add(tratamiento.id)
                        newhistorial.tratamiento.add(tratamiento.id)
                    for vacuna in vacunas:
                        valortotal += vacuna.precio
                        instance_.inyeccion.add(vacuna.id)
                        newhistorial.inyeccion.add(vacuna.id)
                    instance_.precio_total = valortotal
                    instance_.save(request)
                    instance.estado = 2
                    instance.save(request)
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = DetalleCitaForm()
        else:
            return redirect('veterinario:listar_citas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def eliminar_cita(request, pk):
    try:
        instance = get_object_or_404(Cita, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except Cita.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})
def rechazar_cita(request, pk):

    try:
        instance = get_object_or_404(Cita, pk=pk)
        if request.method == 'POST':
            instance.estado = 3
            instance.save(request)
            return JsonResponse({'success': True, 'message': 'Registro rechazado con éxito'})
    except Cita.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})


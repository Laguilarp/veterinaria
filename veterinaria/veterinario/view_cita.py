import json
import datetime
from datetime import datetime, timedelta
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
from veterinario.models import Propietario, Raza, Cita, DetalleCita, HistorialMedico, Veterinario, HistorialDesparasitante, HistorialVacunacion, \
    MedicacionDetalleCita, VacunacionDetalleCita
from veterinario.forms import RazaForm, CitaForm, DetalleCitaForm, DesparasitacionCitaForm, VacunacionCitaForm, MedicacionCitaForm, \
    VacunacionDetalleCitaForm
@login_required
#@validador
def listar_citas(request,search=None):
    try:
        parametros = ''
        veterinario_ = Veterinario.objects.filter(status=True, persona=request.user.persona_set.filter(status=True).first()).first()
        citas = Cita.objects.filter(status=True, veterinario=veterinario_)
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

        paginator = Paginator(citas.order_by('estado', 'fecha_cita', 'hora_cita'), 25)
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
            'form2': MedicacionCitaForm(),
            'form4': VacunacionDetalleCitaForm()
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
                hora_actual = (datetime.now() + timedelta(minutes=10)).time()
                fecha_cita = datetime.strptime(request.POST['fecha_cita'], '%Y-%m-%d').date()
                hora_cita = datetime.strptime(request.POST['hora_cita'], '%H:%M').time()


                #VALIDAMOS FECHA DE LA CITA
                if fecha_cita < fechaactual or (fechaactual == fecha_cita and hora_actual > hora_cita):
                    return JsonResponse({'success': False,
                                         'errors': u'La fecha de la cita debe de ser superior o igual a la fecha actual y la hora 10 minutos superior a la hora actual '})

                #VALIDA HORARIO LABORAL
                if hora_cita.hour < 8:
                    return JsonResponse({'success': False,
                                         'errors': u'El horario laboral es a partir de las 8:00 AM.'})

                if hora_cita.hour > 17:
                    return JsonResponse({'success': False,
                                         'errors': u'El horario laboral finaliza a las 5:00 PM.'})
                elif hora_cita.hour == 17 and hora_cita.minute > 0:
                    return JsonResponse({'success': False,
                                         'errors': u'El horario laboral finaliza a las 5:00 PM.'})


                #SE VALIDA QUE NO EXISTA OTRA CITA CON LA MISMA FECHA Y HORA
                existe_cita = Cita.objects.filter(status=True, fecha_cita=fecha_cita, hora_cita=hora_cita, estado=1)
                if existe_cita.exists():
                    return JsonResponse({'success': False, 'errors': u'Ya existe una cita reservada para la fecha y hora ingresada'})
                elif fecha_cita < fechaactual:
                    return JsonResponse({'success': False, 'errors': u'No puede reservar con fecha inferior a la actual'})
                veterinariosesion = request.user.persona_set.filter(status=True).first()
                veterinario_ = Veterinario.objects.filter(status=True, persona=veterinariosesion).first()
                if not veterinario_:
                    return JsonResponse(
                        {'success': False, 'errors': u'No puede reservar sin ser veterinario'})
                instance = Cita(
                    mascota_id=request.POST['mascota'],
                    veterinario=veterinario_,
                    fecha_cita=fecha_cita,
                    hora_cita=hora_cita,
                    motivocita=request.POST['motivocita'],
                    motivo=request.POST['motivo'],
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
                            <li><strong>Motivo:</strong> {instance.get_motivocita_display()}</li>
                            <li><strong>Observación:</strong> {instance.motivo}</li>
                        </ul>
                        <p>¡Gracias por confiar en MediPets!</p>
                        """

                        enviar_correo(
                            destinatario=propietario.persona.correo_electronico,
                            asunto='Cita agendada!',
                            mensaje=mensaje,
                            archivo=''  # Opcional
                        )
                return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
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
        'scriptCita': True,
        'fechaactual': datetime.now().date(),
        'scriptPropietarioCita': True
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
                veterinariosesion = request.user.persona_set.filter(status=True).first()
                hora_actual = (datetime.now() + timedelta(minutes=10)).time()
                fecha_cita = datetime.strptime(request.POST['fecha_cita'], '%Y-%m-%d').date()
                hora_cita = datetime.strptime(request.POST['hora_cita'], '%H:%M').time()

                # VALIDAMOS FECHA DE LA CITA
                if fecha_cita < fechaactual or (
                        fechaactual == fecha_cita and hora_actual > hora_cita):
                    return JsonResponse({'success': False,
                                         'errors': u'La fecha de la cita debe de ser superior o igual a la fecha actual y la hora 10 minutos superior a la hora actual'})

                # VALIDA HORARIO LABORAL
                if hora_cita.hour < 8:
                    return JsonResponse({'success': False,
                                         'errors': u'El horario laboral es a partir de las 8:00 AM.'})

                if hora_cita.hour > 17:
                    return JsonResponse({'success': False,
                                         'errors': u'El horario laboral finaliza a las 5:00 PM.'})
                elif hora_cita.hour == 17 and hora_cita.minute > 0:
                    return JsonResponse({'success': False,
                                         'errors': u'El horario laboral finaliza a las 5:00 PM.'})

                # SE VALIDA QUE NO EXISTA OTRA CITA CON LA MISMA FECHA Y HORA
                existe_cita = Cita.objects.filter(status=True, fecha_cita=fecha_cita,
                                                  hora_cita=hora_cita, estado=1).exclude(id=instance.id)
                if existe_cita.exists():
                    return JsonResponse(
                        {'success': False, 'errors': u'Ya existe una cita reservada para la fecha y hora ingresada'})
                elif fecha_cita < fechaactual:
                    return JsonResponse(
                        {'success': False, 'errors': u'No puede reservar con fecha inferior a la actual'})
                instance.mascota.id = request.POST['mascota']
                instance.veterinario.persona = veterinariosesion
                instance.fecha_cita = fecha_cita
                instance.hora_cita = hora_cita
                instance.motivocita = request.POST['motivocita']
                instance.motivo = request.POST['motivo']
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
                                                                    <li><strong>Motivo:</strong> {instance.get_motivocita_display()}</li>
                                                                    <li><strong>Observación:</strong> {instance.motivo}</li>
                                                                </ul>
                                                                <p>¡Gracias por confiar en MediPets!</p>
                                                                """

                        enviar_correo(
                            destinatario=propietario.persona.correo_electronico,
                            asunto='Cita agendada!',
                            mensaje=mensaje,
                            archivo=''  # Opcional
                        )
                return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = CitaForm(initial={'mascota': instance.mascota,
                                     'veterinario': instance.veterinario,
                                     'fecha_cita': instance.fecha_cita,
                                     'hora_cita': instance.hora_cita,
                                     'motivocita': instance.motivocita,
                                     'motivo': instance.motivo,
                                     })
        else:
            return redirect('veterinario:listar_citas')

    idPropietarioPre = instance.mascota.get_propietario().id if instance.mascota.get_propietario() else None
    context = {
        'form': form,
        'scriptCita': True,
        'scriptPropietarioCita': True,
        'idMascotaPre': instance.mascota.id,
        'idPropietarioPre': idPropietarioPre
    }
    return render(request, 'form_modal.html', context)

def atender_cita(request, pk):
    instance = get_object_or_404(Cita, pk=pk)
    scriptFechaFechaFab = False
    scriptFechaProximaVacuna = False
    if request.method == 'POST':
        try:
            with transaction.atomic():
                if instance.motivocita == 1:
                    form = VacunacionCitaForm(request.POST, request.FILES)
                elif instance.motivocita == 2:
                    form = DesparasitacionCitaForm(request.POST, request.FILES)
                elif instance.motivocita == 3:
                    form = DetalleCitaForm(request.POST, request.FILES)
                if form.is_valid():

                    if instance.motivocita == 1:
                        # VACUNACIÓN
                        fecha = datetime.now().date()
                        edad = form.cleaned_data['edad']
                        peso = form.cleaned_data['peso']

                        instance_ = DetalleCita(cita=instance, fecha=fecha, edad=edad, peso=peso)
                        instance_.save(request)

                        historial = HistorialVacunacion(veterinario=instance.veterinario, mascota=instance.mascota,
                                                            fecha=fecha, edad=edad, peso=peso)
                        historial.save(request)

                        try:
                            vacunaciones_data = json.loads(request.POST.get('vacunacionesData', '[]'))
                            for data in vacunaciones_data:
                                if datetime.strptime(data['fechaproximavacuna'], '%Y-%m-%d').date() <= fecha:
                                    return JsonResponse({'success': False, 'errors': 'La fecha próxima vacuna seleccionada no puede ser menor o igual a la fecha actual'})
                                newvacuna = VacunacionDetalleCita(
                                    historial=historial,
                                    vacuna_id=data['vacuna'],
                                    lote=data['lote'],
                                    fechafab=data['fechafab'],
                                    fechaproximavacuna=data['fechaproximavacuna'],
                                )
                                newvacuna.save(request)
                        except Exception as ex:
                            pass

                    if instance.motivocita == 2:

                        #DESPARASITANTE
                        fecha = datetime.now().date()
                        edad = form.cleaned_data['edad']
                        peso = form.cleaned_data['peso']
                        desparasitante = form.cleaned_data['desparasitante']
                        fechaproximadesparasitante = form.cleaned_data['fechaproximadesparasitante']

                        instance_ = DetalleCita(cita=instance, fecha=fecha, edad=edad, peso=peso, desparasitante=desparasitante, fechaproximadesparasitante=fechaproximadesparasitante)
                        instance_.save(request)

                        historial = HistorialDesparasitante(veterinario=instance.veterinario, mascota=instance.mascota, fecha=fecha,
                                                            edad=edad, peso=peso, desparasitante=desparasitante,
                                                            fechaproximadesparasitante=fechaproximadesparasitante)
                        historial.save(request)

                    if instance.motivocita == 3:
                        valortotal = 0
                        fecha = datetime.now().date()
                        instance_ = DetalleCita(cita=instance, observacion=request.POST['observacion'])
                        instance_.save(request)
                        newhistorial = HistorialMedico(veterinario=instance.veterinario, mascota=instance.mascota,
                                                       descripcion=request.POST['observacion'],
                                                       fecha_consulta=fecha)
                        newhistorial.save(request)
                        try:
                            medicaciones_data = json.loads(request.POST.get('medicacionesData', '[]'))
                            for data in medicaciones_data:
                                newmedicacion = MedicacionDetalleCita(
                                    detalle=newhistorial,
                                    medicamento_id=data['medicamento'],
                                    dosis=data['dosis'],
                                    prescripcion=data['prescripcion'],
                                )
                                newmedicacion.save(request)
                        except Exception as ex:
                            pass
                        instance_.save(request)

                    instance.estado = 2
                    instance.save(request)
                    propietario = instance.mascota.get_propietario()
                    if propietario:
                        if propietario.persona.correo_electronico:
                            # Usar la función
                            mensaje = f"""
                                        <h1>¡Hola, {propietario.__str__()}!</h1>
                                        <p>Tu cita se ha atendido correctamente en <strong>Medipets</strong>.</p>
                                        <p><strong>Detalles de tu cita:</strong></p>
                                        <ul>
                                            <li><strong>Fecha:</strong> {instance.fecha_cita}</li>
                                            <li><strong>Hora:</strong> {instance.hora_cita}</li>
                                            <li><strong>Mascota:</strong> {instance.mascota.__str__()}</li>
                                            <li><strong>Motivo consulta:</strong> {instance.get_motivocita_display()}</li>
                                            <li><strong>Observación:</strong> {instance.motivo}</li>
                                        </ul>
                                        <p>¡Gracias por confiar en MediPets!</p>
                                        """

                            enviar_correo(
                                destinatario=propietario.persona.correo_electronico,
                                asunto='Cita atendida!',
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
        form2 = None
        addtablemedicacion = False
        addtablevacunacion = False
        if is_ajax(request):
            if instance.motivocita == 1:
                form = VacunacionCitaForm()
                addtablevacunacion = True
                scriptFechaFechaFab = True
                scriptFechaProximaVacuna = True
            elif instance.motivocita == 2:
                form = DesparasitacionCitaForm()
            elif instance.motivocita == 3:
                form = DetalleCitaForm()
                addtablemedicacion = True
        else:
            return redirect('veterinario:listar_citas')
    context = {
        'form': form,
        'addtablemedicacion': addtablemedicacion,
        'addtablevacunacion': addtablevacunacion,
        'scriptFechaFechaFab': scriptFechaFechaFab,
        'scriptFechaProximaVacuna': scriptFechaProximaVacuna,
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
            propietario = instance.mascota.get_propietario()
            if propietario:
                if propietario.persona.correo_electronico:
                    # Usar la función
                    mensaje = f"""
                                <h1>¡Hola, {propietario.__str__()}!</h1>
                                <p>Tu cita se ha rechazado en <strong>Medipets</strong>.</p>
                                <p><strong>Detalles de tu cita:</strong></p>
                                <ul>
                                    <li><strong>Fecha:</strong> {instance.fecha_cita}</li>
                                    <li><strong>Hora:</strong> {instance.hora_cita}</li>
                                    <li><strong>Mascota:</strong> {instance.mascota.__str__()}</li>
                                    <li><strong>Motivo:</strong> {instance.get_motivocita_display()}</li>
                                    <li><strong>Observación:</strong> {instance.motivo}</li>
                                </ul>
                                <p>¡Gracias por confiar en MediPets!</p>
                                """

                    enviar_correo(
                        destinatario=propietario.persona.correo_electronico,
                        asunto='Cita rechazada!',
                        mensaje=mensaje,
                        archivo=''  # Opcional
                    )
            return JsonResponse({'success': True, 'message': 'Registro rechazado con éxito'})
    except Cita.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})


def cargar_mascotas(request):
    propietario_id = request.GET.get('propietario_id')
    propietario = Propietario.objects.get(id=propietario_id)
    mascotas = propietario.mascota.filter(status=True)
    mascotas_json = [{'id': mascota.id, 'nombre': mascota.nombre} for mascota in mascotas]
    return JsonResponse({'mascotas': mascotas_json})


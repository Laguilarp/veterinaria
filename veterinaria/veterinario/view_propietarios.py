import json
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
from django.contrib.auth.models import User
from veterinario.models import Propietario, Mascota
from veterinario.forms import AddMascotaForm, PersonaForm, MascotaForm, MascotaPropietarioForm

def calcular_usuario(persona, variant=1):
    def clean_and_normalize(text):
        # Esta función limpia y normaliza el texto eliminando espacios y caracteres especiales
        return ''.join(c.lower() for c in text if c.isalnum())

    # Obtener los nombres y apellidos de la persona
    nombres = persona.nombres.lower().split()
    apellido1 = persona.apellido1.lower()
    apellido2 = persona.apellido2.lower() if persona.apellido2 else ''

    # Generar el nombre de usuario
    username = clean_and_normalize(f"{nombres[0][0]}{apellido1}{apellido2[0]}")

    # Verificar si el nombre de usuario ya existe en la base de datos
    if not User.objects.filter(username=username).exclude(persona=persona).exists():
        return username
    else:
        # Si ya existe, agregar un número incremental hasta encontrar un nombre de usuario único
        variant = 1
        while True:
            variant_username = f"{username}{variant}"
            if not User.objects.filter(username=variant_username).exclude(persona=persona).exists():
                return variant_username
            variant += 1

@login_required
#@validador
def listar_propietarios(request,search=None):
    try:
        parametros = ''
        propietarios = Propietario.objects.filter(status=True)
        if 'search' in request.GET:
            search_ = search = request.GET['search']
            parametros += '&search=' + search_
            search_ = search_.strip()
            ss = search_.split(' ')
            if len(ss) == 1:
                propietarios = propietarios.filter(Q(persona__nombres__icontains=search) |
                                           Q(persona__apellido1__icontains=search) |
                                           Q(persona__apellido2__icontains=search) |
                                           Q(persona__documento__icontains=search))
            else:
                propietarios = propietarios.filter((Q(persona__apellido1__icontains=ss[0]) & Q(persona__apellido2__icontains=ss[1])) |
                                           (Q(persona__nombres__icontains=ss[0]) & Q(persona__nombres__icontains=ss[1])))

        paginator = Paginator(propietarios, 25)
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'page_object': page_object,
            'page_titulo': "Propietarios",
            'titulo': "Propietarios",
            'search': search,
            'parametros': parametros,
            'form2': MascotaForm(),
        }
        return render(request, 'propietarios/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")


@login_required
def crear_propietario(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                #W
                form = PersonaForm(request.POST, request.FILES)
                form2 = AddMascotaForm(request.POST)
                if form.is_valid():
                    if len(str(form.cleaned_data['documento'])) != 10:
                        return JsonResponse({'success': False, 'errors': 'Cèdula no vàlida'})
                    hoy = datetime.now().date()
                    fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    # Calcular la edad
                    edad_base = 15
                    edad = hoy.year - fecha_nacimiento.year - (
                                (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
                    if edad < edad_base:
                        return JsonResponse({'success': False,
                                             'errors': 'La persona es menor a 15 años'})
                    if Persona.objects.filter(status=True, documento=form.cleaned_data['documento']).exists():
                        return JsonResponse({'success': False, 'errors': 'La persona ya se encuentra registrada con la misma identificaciòn'})
                    instance = Persona(
                        nombres=form.cleaned_data['nombres'],
                        apellido1=form.cleaned_data['apellido1'],
                        apellido2=form.cleaned_data['apellido2'],
                        tipodocumento=form.cleaned_data['tipodocumento'],
                        documento=form.cleaned_data['documento'],
                        direccion=form.cleaned_data['direccion'],
                        genero=form.cleaned_data['genero'],
                        fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                        correo_electronico=form.cleaned_data['correo_electronico'],
                        telefono=form.cleaned_data['telefono'],
                    )
                    instance.save(request)
                    identificacion = '*'
                    if instance.documento:
                        identificacion = instance.documento
                    password = identificacion.replace(' ', '')
                    password = password.lower()
                    username = calcular_usuario(instance)
                    usuario = User.objects.create_user(username, password)
                    usuario.save()
                    instance.usuario = usuario
                    instance.save(request)
                    persona_perfil = PersonaPerfil(
                        persona=instance
                    )
                    persona_perfil.save(request)
                    newpropietario = Propietario(persona=instance)
                    newpropietario.save(request)
                    try:
                        mascotas_data = json.loads(request.POST.get('mascotasData', '[]'))
                        for data in mascotas_data:
                            newmascota = Mascota(
                                nombre=data['nombre'],
                                sexo_id=data['sexo'],
                                raza_id=data['raza'],
                                color=data['color'],
                                peso=data['peso'],
                            )
                            newmascota.save(request)
                            newpropietario.mascota.add(newmascota)
                    except Exception as ex:
                        pass

                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = PersonaForm()
            form2 = MascotaForm()
        else:
            return redirect('administrativo:listar_personas')
    context = {
        'form': form,
        'addtable': True,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_propietario(request, pk):
    instance = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = PersonaForm(request.POST, request.FILES)
                form2 = AddMascotaForm(request.POST)
                if form.is_valid():
                    if len(str(form.cleaned_data['documento'])) != 10:
                        return JsonResponse({'success': False, 'errors': 'Cèdula no vàlida'})
                    hoy = datetime.now().date()
                    fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    # Calcular la edad
                    edad_base = 15
                    edad = hoy.year - fecha_nacimiento.year - (
                                (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
                    if edad < edad_base:
                        return JsonResponse({'success': False,
                                             'errors': 'La persona es menor a 15 años'})
                    if Persona.objects.filter(status=True, documento=form.cleaned_data['documento']).exclude(id=instance.id).exists():
                        return JsonResponse({'success': False, 'errors': 'La persona ya se encuentra registrada con la misma identificaciòn'})
                    lista_mascotas = request.POST.getlist('mascota')
                    instance.nombres = form.cleaned_data['nombres']
                    instance.apellido1 = form.cleaned_data['apellido1']
                    instance.apellido2 = form.cleaned_data['apellido2']
                    instance.tipodocumento = form.cleaned_data['tipodocumento']
                    instance.documento = form.cleaned_data['documento']
                    instance.direccion = form.cleaned_data['direccion']
                    instance.genero = form.cleaned_data['genero']
                    instance.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    instance.correo_electronico = form.cleaned_data['correo_electronico']
                    instance.telefono = form.cleaned_data['telefono']
                    instance.save(request)

                    propietario = Propietario.objects.get(persona=instance)
                    lista_mis_mascotas = request.POST.getlist('mismascotas')
                    # Eliminar todas las relaciones con las mascotas de ese propietario
                    id_mascotas = propietario.mascota.filter(status=True).exclude(id__in=lista_mis_mascotas).values_list('id', flat=True)
                    desvincula_propietarios = Mascota.objects.filter(status=True, id__in=id_mascotas).update(status=False)
                    for id_mascota_ in id_mascotas:
                        propietario.mascota.remove(id_mascota_)

                    try:
                        mascotas_data = json.loads(request.POST.get('mascotasData', '[]'))
                        for data in mascotas_data:
                            newmascota = Mascota(
                                nombre=data['nombre'],
                                sexo_id=data['sexo'],
                                raza_id=data['raza'],
                                color=data['color'],
                                peso=data['peso'],
                            )
                            newmascota.save(request)
                            propietario.mascota.add(newmascota)
                    except Exception as ex:
                        pass

                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = PersonaForm(initial={
                                        'nombres': instance.nombres,
                                        'apellido1': instance.apellido1,
                                        'apellido2': instance.apellido2,
                                        'tipodocumento': instance.tipodocumento,
                                        'documento': instance.documento,
                                        'direccion': instance.direccion,
                                        'genero': instance.genero,
                                        'fecha_nacimiento': instance.fecha_nacimiento.strftime('%Y-%m-%d'),
                                        'correo_electronico': instance.correo_electronico,
                                        'telefono': instance.telefono,
            })
            propietario = Propietario.objects.get(persona=instance)
            mascotas_ = propietario.mascota.filter(status=True)
        else:
            return redirect('administrativo:listar_personas')
    form.bloquear_campos()
    context = {
        'form': form,
        'mismascotas': mascotas_,
        'addtable': True,
    }
    return render(request, 'form_modal.html', context)

@login_required
def eliminar_propietario(request, pk):
    try:
        instance = get_object_or_404(Propietario, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except Propietario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})

@login_required
def resetear_clave(request):
    try:
        with transaction.atomic():
            persona = Propietario.objects.get(pk=request.POST['id'])
            persona.persona.usuario.set_password(str(persona.get_card_id()))
            persona.persona.usuario.save()
            return JsonResponse({'success': True, 'message': 'Clave reseteada correctamente'})

    except Exception as ex:
        transaction.set_rollback(True)
        return JsonResponse({'success': False, 'message': 'Error al resetear la clave'})


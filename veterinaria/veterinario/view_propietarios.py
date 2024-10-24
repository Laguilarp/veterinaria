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
from baseapp.forms import PersonaForm
from django.contrib.auth.models import User
from veterinario.models import Propietario

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
                                           Q(persona__cedula__icontains=search) |
                                           Q(persona__pasaporte__icontains=search))
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
        }
        return render(request, 'propietarios/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")


@login_required
def crear_propietario(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = PersonaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = Persona(
                        nombres=form.cleaned_data['nombres'],
                        apellido1=form.cleaned_data['apellido1'],
                        apellido2=form.cleaned_data['apellido2'],
                        cedula=form.cleaned_data['cedula'],
                        pasaporte=form.cleaned_data['pasaporte'],
                        ruc=form.cleaned_data['ruc'],
                        direccion=form.cleaned_data['direccion'],
                        genero=form.cleaned_data['genero'],
                        fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                        correo_electronico=form.cleaned_data['correo_electronico'],
                        telefono=form.cleaned_data['telefono'],
                    )
                    instance.save(request)
                    if 'foto' in request.FILES:
                        archivo = request.FILES['foto']
                        archivo._name = "fotoperfil_" + str(instance.id) + '_' + str(datetime.now())
                        instance.foto = archivo
                        instance.save(request)
                    identificacion = '*'
                    if instance.cedula:
                        identificacion = instance.cedula
                    elif instance.pasaporte:
                        identificacion = instance.pasaporte
                    elif instance.ruc:
                        identificacion = instance.ruc
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
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = PersonaForm()
        else:
            return redirect('administrativo:listar_personas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_propietario(request, pk):
    instance = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = PersonaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance.nombres = form.cleaned_data['nombres']
                    instance.apellido1 = form.cleaned_data['apellido1']
                    instance.apellido2 = form.cleaned_data['apellido2']
                    instance.cedula = form.cleaned_data['cedula']
                    instance.pasaporte = form.cleaned_data['pasaporte']
                    instance.ruc = form.cleaned_data['ruc']
                    instance.direccion = form.cleaned_data['direccion']
                    instance.genero = form.cleaned_data['genero']
                    instance.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    instance.correo_electronico = form.cleaned_data['correo_electronico']
                    instance.telefono = form.cleaned_data['telefono']
                    instance.save(request)
                    if 'foto' in request.FILES:
                        archivo = request.FILES['foto']
                        extension = archivo._name[archivo._name.rfind("."):]
                        archivo._name = "fotoperfil_" + str(instance.id) + '_' + str(datetime.now()).replace('-', '_') + extension.lower()
                        instance.foto = archivo
                        instance.save(request)
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
                                        'cedula': instance.cedula,
                                        'pasaporte': instance.pasaporte,
                                        'ruc': instance.ruc,
                                        'direccion': instance.direccion,
                                        'genero': instance.genero,
                                        'fecha_nacimiento': instance.fecha_nacimiento.strftime('%Y-%m-%d'),
                                        'correo_electronico': instance.correo_electronico,
                                        'telefono': instance.telefono,
                                        'foto': instance.foto,
            })
        else:
            return redirect('administrativo:listar_personas')
    form.bloquear_campos()
    context = {
        'form': form,
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


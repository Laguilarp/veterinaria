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
from veterinario.models import Propietario, Mascota
from veterinario.forms import MascotaForm

@login_required
#@validador
def listar_mascotas(request,search=None):
    try:
        parametros = ''
        mascotas = Mascota.objects.filter(status=True)
        if 'search' in request.GET:
            search_ = search = request.GET['search']
            parametros += '&search=' + search_
            search_ = search_.strip()
            ss = search_.split(' ')
            if len(ss) == 1:
                mascotas = mascotas.filter(Q(nombre__icontains=search))
            else:
                mascotas = mascotas.filter(Q(nombre__icontains=ss[0]))

        paginator = Paginator(mascotas, 25)
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'page_object': page_object,
            'page_titulo': "Mascotas",
            'titulo': "Mascotas",
            'search': search,
            'parametros': parametros,
        }
        return render(request, 'mascota/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")


@login_required
def crear_mascota(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = MascotaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = Mascota(
                        nombre=form.cleaned_data['nombre'],
                        especie=form.cleaned_data['especie'],
                        sexo=form.cleaned_data['sexo'],
                        raza=form.cleaned_data['raza'],
                        color=form.cleaned_data['color'],
                        fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                        peso=form.cleaned_data['peso']
                    )
                    instance.save(request)
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = MascotaForm()
        else:
            return redirect('veterinario:listar_mascotas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_mascota(request, pk):
    instance = get_object_or_404(Mascota, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = MascotaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance.nombre = form.cleaned_data['nombre']
                    instance.especie = form.cleaned_data['especie']
                    instance.sexo = form.cleaned_data['sexo']
                    instance.raza = form.cleaned_data['raza']
                    instance.color = form.cleaned_data['color']
                    instance.fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
                    instance.peso = form.cleaned_data['peso']
                    instance.save(request)
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = MascotaForm(initial={
                                        'nombre': instance.nombre,
                                        'especie': instance.especie,
                                        'sexo': instance.sexo,
                                        'raza': instance.raza,
                                        'color': instance.color,
                                        'fecha_nacimiento': instance.fecha_nacimiento.strftime('%Y-%m-%d'),
                                        'peso': instance.peso
            })
        else:
            return redirect('veterinario:listar_mascotas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def eliminar_mascota(request, pk):
    try:
        instance = get_object_or_404(Mascota, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except Mascota.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})


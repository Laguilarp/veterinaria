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
from veterinario.models import Propietario, Raza, SexoMascota
from veterinario.forms import RazaForm, SexoMascotaForm
@login_required
#@validador
def listar_sexo(request,search=None):
    try:
        parametros = ''
        sexos = SexoMascota.objects.filter(status=True)
        if 'search' in request.GET:
            search_ = search = request.GET['search']
            parametros += '&search=' + search_
            search_ = search_.strip()
            ss = search_.split(' ')
            if len(ss) == 1:
                sexos = sexos.filter(Q(nombre__icontains=search))
            else:
                sexos = sexos.filter(Q(nombre__icontains=ss[0]))

        paginator = Paginator(sexos, 25)
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'page_object': page_object,
            'page_titulo': "Sexos",
            'titulo': "Sexos",
            'search': search,
            'parametros': parametros,
        }
        return render(request, 'sexomascota/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")


@login_required
def crear_sexo(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = RazaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = SexoMascota(
                        nombre=form.cleaned_data['nombre'],
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
            form = SexoMascotaForm()
        else:
            return redirect('veterinario:listar_razas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_sexo(request, pk):
    instance = get_object_or_404(SexoMascota, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = SexoMascotaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance.nombre = form.cleaned_data['nombre']
                    instance.save(request)
                    return JsonResponse({'success': True, 'message': 'Acción realizada con éxito!'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({'success': False})
    else:
        if is_ajax(request):
            form = SexoMascotaForm(initial={'nombre': instance.nombre})
        else:
            return redirect('vete:listar_razas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def eliminar_sexo(request, pk):
    try:
        instance = get_object_or_404(SexoMascota, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except SexoMascota.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})


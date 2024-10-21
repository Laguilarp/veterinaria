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
from core.core import DIAS_SEMANA
from administrativo.models import Cargo
from administrativo.forms import CargoForm
from authenticaction.models import CustomUser


@login_required
@validador
def listar_cargos(request,search=None):
    try:
        parametros = ''
        cargos = Cargo.objects.filter(status=True)
        if 'search' in request.GET:
            search_ = search = request.GET['search']
            parametros += '&search=' + search_
            search_ = search_.strip()
            ss = search_.split(' ')
            cargos = cargos.filter(Q(nombre__icontains=search))

        paginator = Paginator(cargos, 25)
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'page_object': page_object,
            'page_titulo': "Cargos",
            'titulo': "Cargos",
            'search': search,
            'parametros': parametros,
        }
        return render(request, 'cargos/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")

@login_required
def crear_cargo(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = CargoForm(request.POST)
                if form.is_valid():
                    instance = Cargo(
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
            form = CargoForm()
        else:
            return redirect('administrativo:listar_jornadas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_cargo(request, pk):
    instance = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = CargoForm(request.POST, instance=instance)
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
            form = CargoForm(initial={
                'nombre': instance.nombre,
            })
        else:
            return redirect('administrativo:listar_jornadas')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def eliminar_cargo(request, pk):
    try:
        instance = get_object_or_404(Cargo, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except Cargo.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})

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
from veterinario.models import Propietario, Raza, TipoEspecie
from veterinario.forms import EspecieForm
@login_required
#@validador
def listar_especies(request,search=None):
    try:
        parametros = ''
        especies = TipoEspecie.objects.filter(status=True)
        if 'search' in request.GET:
            search_ = search = request.GET['search']
            parametros += '&search=' + search_
            search_ = search_.strip()
            ss = search_.split(' ')
            if len(ss) == 1:
                especies = especies.filter(Q(nombre__icontains=search))
            else:
                especies = especies.filter(Q(nombre__icontains=ss[0]))

        paginator = Paginator(especies, 25)
        page = request.GET.get('page')
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'page_object': page_object,
            'page_titulo': "Tipo especies",
            'titulo': "Tipo especies",
            'search': search,
            'parametros': parametros,
        }
        return render(request, 'especie/inicio.html', context)
    except Exception as e:
        HttpResponseRedirect(f"/?info={e.__str__()}")


@login_required
def crear_especie(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = EspecieForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = TipoEspecie(
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
            form = EspecieForm()
        else:
            return redirect('veterinario:listar_especies')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def editar_especie(request, pk):
    instance = get_object_or_404(TipoEspecie, pk=pk)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                form = EspecieForm(request.POST, request.FILES)
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
            form = EspecieForm(initial={'nombre': instance.nombre})
        else:
            return redirect('veterinario:listar_especies')
    context = {
        'form': form,
    }
    return render(request, 'form_modal.html', context)

@login_required
def eliminar_especie(request, pk):
    try:
        instance = get_object_or_404(TipoEspecie, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except TipoEspecie.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})


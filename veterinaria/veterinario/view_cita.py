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
from veterinario.models import Propietario, Raza, Cita, DetalleCita
from veterinario.forms import RazaForm, CitaForm
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
                citas = citas.filter(Q(nombre__icontains=search))
            else:
                citas = citas.filter(Q(nombre__icontains=ss[0]))

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
                form = CitaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = Cita(
                        mascota=form.cleaned_data['mascota'],
                        propietario=form.cleaned_data['mascota'].propietario,
                        veterinario=form.cleaned_data['veterinario'],
                        fecha_cita=form.cleaned_data['fecha_cita'],
                        hora_cita=form.cleaned_data['hora_cita'],
                        motivo=form.cleaned_data['motivo'],
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
                form = CitaForm(request.POST, request.FILES)
                if form.is_valid():
                    instance.mascota = form.cleaned_data['mascota']
                    instance.veterinario = form.cleaned_data['veterinario']
                    instance.fecha_cita = form.cleaned_data['fecha_cita']
                    instance.hora_cita = form.cleaned_data['hora_cita']
                    instance.motivo = form.cleaned_data['motivo']
                    instance.save(request)
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

@login_required
def eliminar_cita(request, pk):
    try:
        instance = get_object_or_404(Cita, pk=pk)
        if request.method == 'POST':
            instance.eliminar_registro(request)
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito'})
    except Cita.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El registro no existe'})


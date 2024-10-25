from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from authenticaction.forms import CustomUserCreationForm, CustomLoginForm
from authenticaction.models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Cambia 'home' a la página de inicio de tu aplicación
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', '')  # Obtener la URL de redirección desde el parámetro 'next'
                    if next_url:
                        return HttpResponseRedirect(next_url)  # Redirigir a la URL especificada
                    return redirect('home')  # Redirigir al usuario a la página de inicio después del inicio de sesión
                else:
                    messages.error(request, 'Tu cuenta está desactivada. Por favor, contacta al administrador.')
            else:
                messages.error(request, 'Tu cuenta no se encuentra autenticada.')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = CustomLoginForm(request)

    context = {
        'page_titulo': 'Inicio de sesión',
        'form': form,
    }
    return render(request, 'registration/login.html',context)


def custom_logout(request):
    logout(request)
    return redirect('/')  # Cambia 'login' a la página de inicio de sesión de tu aplicación

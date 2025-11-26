from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Enviar email de bienvenida
            try:
                send_mail(
                    subject='Bienvenido al Sistema de Gestión Educativa',
                    message=f'Hola {user.username},\n\n'
                            f'¡Bienvenido al Sistema de Gestión Educativa!\n\n'
                            f'Tu cuenta ha sido creada exitosamente.\n'
                            f'Ya puedes iniciar sesión y comenzar a gestionar tus alumnos.\n\n'
                            f'Saludos cordiales,\n'
                            f'El equipo de Sistema Educativo',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error enviando email: {e}")
            
            messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')
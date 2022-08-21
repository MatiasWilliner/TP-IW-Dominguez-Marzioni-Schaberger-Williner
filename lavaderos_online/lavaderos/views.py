from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# Página de inicio del sitio.
def inicio(request):
    return render(request, 'inicio.html', {})

@login_required(login_url='/cuentas/login/')
def perfil(request):
    return render(request, 'perfil.html', {})

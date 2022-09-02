from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.

# Página de inicio del sitio.
def inicio(request):
    print ("Hola mundo")
    return render(request, 'inicio.html', {})

#NICO
def basic(request):
    return render(request,'basic.html',{})
    
    
    
    
#NICO
def lavadero(request):
    return render(request,'lavadero.html',{})

#NICO
def registroLavadero(request):
    return render(request,'registroLavadero.html',{})


@login_required(login_url='/cuentas/login/')
def perfil(request):
    return render(request, 'perfil.html', {})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro exitoso!")
            return redirect("inicio")
        messages.error(request, "Registro sin éxito. Información inválida.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})

from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, NewLavaderoForm, NewTarifaForm
from .models import Lavadero
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from lavaderos.models import *
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from lavaderos.tokens import account_activation_token
# Create your views here.

# Página de inicio del sitio.
def inicio(request):
    if request.user.is_authenticated:
        return redirect("lavaderos")
    print ("Hola mundo")
    return render(request, 'inicio.html', {})

#NICO
def basic(request):
    user = request.user
    featured_filter = 'T'
    if request.GET.get('estado'):
        featured_filter = request.GET.get('estado')
        if featured_filter == 'T':
            lavadero = Lavadero.objects.exclude(estado='I')
        else:
            lavadero = Lavadero.objects.filter(estado=featured_filter)
    else:
        lavadero = Lavadero.objects.exclude(estado='I')
    return render(request,'basic.html',{'lavaderolist':lavadero,'estadoselect':featured_filter,"user":user})
    
    
#NICO
def lavadero(request,id):
    print('ENTRO A LAVADERO')
    try:
        lavadero = Lavadero.objects.get(pk=id)
    except Lavadero.DoesNotExist:
        lavadero = None
    if lavadero:
        return render(request, 'lavadero.html', {'lavadero': lavadero})
    else:
        print(lavadero)
        return redirect("lavaderos")



#NICO
@login_required(login_url='/cuentas/login/')
def registroLavadero(request):

    user = request.user
    form = NewLavaderoForm()
    formulario = NewTarifaForm()
    if request.method == "POST":
        form = NewLavaderoForm(request.POST, request.FILES)
        if form.is_valid():
            lavadero = form.save(commit=False)
            lavadero.creado_por = user

            lavadero.save()
            return redirect("inicio")
    return render(request=request,template_name='registroLavadero.html', context={"tarifas_lavadero":formulario, "register_lavadero":form})



@login_required(login_url='/cuentas/login/')
def perfil(request):
    return render(request, 'perfil.html', {})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))                       
            return redirect('inicio')
        messages.error(request, "Registro sin éxito. Información inválida.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})


def activateEmail(request, user, to_email):
    mail_subject = 'Confirma tu cuenta de Lavadero Online!.'
    message = render_to_string('template_confirmar_mail.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(request, f'Bienvenido <b>{user}</b>, dirijase a su bandeja de entrada: <b>{to_email}</b> y presione el boton confirmar cuenta ')
    else:
        messages.error(request, f'Ha ocurrido un error enviado un mail a {to_email}')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Gracias por confirmar tu cuenta. Ya puedes iniciar sesión en tu cuenta.')
        return redirect('login')
    else:
        messages.error(request, 'Link de activación inválido!')
    
    return redirect('inicio')
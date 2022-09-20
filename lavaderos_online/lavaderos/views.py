from datetime import datetime, time
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, NewLavaderoForm, NewTarifaForm
from .models import Lavadero
from django.forms import formset_factory, inlineformset_factory
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

# LANDINGPAGE #Si el usuario está registrado se redigirá al home(ListadoLavadero) Sino LandingPage
def inicio(request):
    if request.user.is_authenticated:
        return redirect("lavaderos")
    return render(request, 'inicio.html', {})










# HOME - LISTADO LAVADEROS #No nesesita estar logueado para acceder a esta parte #Si esta logueado tendrá un sidebar con opciones extras
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
    
    







# PERFIL DE LAVADERO  #Muestra la info de cada Lavadero de forma detallada #Si es un usuario cliente podrá solicitar Atención # Si es dueño del lavadero edbería poder editar esta info
def lavadero(request,id):
    print('ENTRO A LAVADERO')
    try:
        lavadero = Lavadero.objects.get(pk=id)

        tarifas = Tarifa.objects.filter(lavadero=lavadero)
        tarifaMoto = tarifas.get(tipo='M')
        tarifaAuto = tarifas.get(tipo='A')
        tarifaPickup = tarifas.get(tipo='P')
        tarifaCamion = tarifas.get(tipo='C')
        
        horarios = Horario.objects.filter(lavadero=lavadero)
        lunes = horarios.get(dia='L')
        martes = horarios.get(dia='M')
        miercoles = horarios.get(dia='X')
        jueves = horarios.get(dia='J')
        viernes = horarios.get(dia='V')
        sabado = horarios.get(dia='S')
        domingo = horarios.get(dia='D')

        context = {
            'lavadero': lavadero,
            'tarifaMoto' : tarifaMoto,
            'tarifaAuto' : tarifaAuto,
            'tarifaPickup' : tarifaPickup,
            'tarifaCamion' : tarifaCamion,
            'lunes' : lunes,
            'martes' : martes,
            'miercoles': miercoles,
            'jueves' : jueves,
            'viernes' : viernes,
            'sabado' : sabado,
            'domingo' : domingo
        }            
    except Lavadero.DoesNotExist:
        lavadero = None
    if lavadero:
        return render(request, 'lavadero.html', context)
    else:
        print(lavadero)
        return redirect("lavaderos")



#NICO
@login_required(login_url='/cuentas/login/')
def registroLavadero(request):    
    user = request.user
    usuario_tiene_lavadero = Lavadero.objects.filter(creado_por=user).exists()
    form = NewLavaderoForm()
    formulario = NewTarifaForm()
    if request.method == "POST":
        form = NewLavaderoForm(request.POST, request.FILES)
        if form.is_valid():
            lavadero = form.save(commit=False)
            lavadero.creado_por = user
            lavadero.save()

            for i in range(4):
                init_tarifa = Tarifa()
                init_tarifa.tipo = init_tarifa.TIPOS_LAVADO[i][0]
                init_tarifa.monto = 0.0
                init_tarifa.lavadero = lavadero
                init_tarifa.save()
            
            for i in range(7):
                init_horario = Horario()
                init_horario.dia = init_horario.DIAS[i][0]
                init_horario.desde = time(0,0,0)
                init_horario.hasta = time(0,0,0)
                init_horario.lavadero = lavadero
                init_horario.save()

            return redirect("milavadero")
    return render(request=request,template_name='registroLavadero.html', context={"tarifas_lavadero":formulario, "register_lavadero":form, "tiene_lavadero":usuario_tiene_lavadero})



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

@login_required(login_url='/cuentas/login/')
def miLavadero(request):
    try:
        user = request.user
        lavadero = Lavadero.objects.get(creado_por=user)
        TarifaInlineFormset = inlineformset_factory(Lavadero, Tarifa, fields=('tipo', 'monto',), extra=0, can_delete=False)
        HorarioInlineFormset = inlineformset_factory(Lavadero, Horario, fields=('dia', 'desde', 'hasta'), extra=0, can_delete=False)
        EstadoInlineFormset = inlineformset_factory(User, Lavadero, fields=('estado',), extra=0, can_delete=False)
    except Lavadero.DoesNotExist:
        lavadero = None
    if lavadero:
        formset_tarifa = TarifaInlineFormset(instance=lavadero)
        formset_horario = HorarioInlineFormset(instance=lavadero)
        formset_estado = EstadoInlineFormset(instance=user)
        if request.method == "POST" and 'submitTarifa' in request.POST:
            formset_tarifa = TarifaInlineFormset(request.POST, instance=lavadero)
            if formset_tarifa.is_valid():
                formset_tarifa.save()
                return redirect("milavadero")
        elif request.method == "POST" and 'submitHorario' in request.POST:
            formset_horario = HorarioInlineFormset(request.POST, instance=lavadero)
            if formset_horario.is_valid():
                formset_horario.save()
                return redirect("milavadero")
        elif request.method == "POST" and 'submitEstado' in request.POST:
            formset_estado = EstadoInlineFormset(request.POST, instance=user)
            if formset_estado.is_valid():
                formset_estado.save()
                return redirect("milavadero")
            
        return render(request, 'milavadero.html', {'tarifa_form':formset_tarifa, 'horario_form':formset_horario, 'estado_form':formset_estado})
    else:
        return redirect("lavaderos")      







































































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
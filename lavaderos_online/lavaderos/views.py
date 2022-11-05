from datetime import datetime, time
from unicodedata import name
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm, NewLavaderoForm, NewTarifaForm, NewSolicitarLavado, NewLavaderoFormA
from .models import Lavadero , SolicitudLavadero
from django.forms import inlineformset_factory
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from lavaderos.models import *
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from lavaderos.tokens import account_activation_token
from django import forms
# Create your views here.

# LANDINGPAGE #Si el usuario está registrado se redigirá al home(ListadoLavadero) Sino LandingPage
def inicio(request):
    if request.user.is_authenticated:
        return redirect("lavaderos")
    return render(request, 'inicio.html', {})


# HOME - LISTADO LAVADEROS #No nesesita estar logueado para acceder a esta parte #Si esta logueado tendrá un sidebar con opciones extras
def basic(request):
    user = request.user
    lavadero_user_register = len(Lavadero.objects.filter(id = request.user.id))
    cantidad_solicitudes_pendientes = len(SolicitudLavadero.objects.filter(lavadero_id = request.user.id, aceptado = None))
    print(cantidad_solicitudes_pendientes)
    
    featured_filter = 'T'
    if request.GET.get('estado'):
        featured_filter = request.GET.get('estado')
        if featured_filter == 'T':
            lavadero = Lavadero.objects.exclude(estado='I')
        else:
            lavadero = Lavadero.objects.filter(estado=featured_filter)
    else:
        lavadero = Lavadero.objects.exclude(estado='I')
    return render(request,'basic.html',{'cantidad_solicitudes_pendientes': cantidad_solicitudes_pendientes,'lavaderolist':lavadero,'estadoselect':featured_filter,"user":user, "lavadero_user_register":lavadero_user_register})
    
    
# PERFIL DE LAVADERO  #Muestra la info de cada Lavadero de forma detallada #Si es un usuario cliente podrá solicitar Atención # Si es dueño del lavadero edbería poder editar esta info
def lavadero(request,id):
    print(request.user)

    print(type(request.user))
    print('ENTRO A LAVADERO')
    lavadero_user_register = len(Lavadero.objects.filter(id = request.user.id))
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

        #DETERMINO SI TIENE UNA SOLICITUD DE LAVADO SIN RESPONDER PARA NO MOSTRAR EL BOTON DE SOLICITAR LAVADO YA Y EVITAR EL FLOOD
        if not request.user.is_anonymous:
            esperando_solicitud = SolicitudLavadero.objects.filter(cliente=request.user, lavadero=lavadero, aceptado=None).exists()
        else:
            esperando_solicitud = True
        print(esperando_solicitud)
        context = {
            'lavadero_user_register' :lavadero_user_register,
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
            'domingo' : domingo,
            'esperando_solicitud' : esperando_solicitud,
        }            
    except Lavadero.DoesNotExist:
        lavadero = None
    if lavadero:
        if request.method == "POST":
            print('post')
            form_solicitar_lavado = NewSolicitarLavado(request.POST)
            if form_solicitar_lavado.is_valid():
                print("es form valido")
                solicitud = form_solicitar_lavado.save(commit=False)
                solicitud.lavadero = lavadero
                solicitud.cliente = request.user
                solicitud.aceptado = None
                solicitud.save()
                mailDueño(request, lavadero.creado_por, lavadero.creado_por.email, request.user, solicitud)
                context['solicitar_lavado'] = form_solicitar_lavado
                return render(request, template_name='lavadero.html', context=context)
        else:
            context['solicitar_lavado'] = NewSolicitarLavado()
            return render(request, 'lavadero.html', context)
    else:
        print(lavadero)
        return redirect("lavaderos")


#NICO
@login_required(login_url='/cuentas/login/')
def registroLavadero(request):    
    user = request.user
    lavadero_user_register = len(Lavadero.objects.filter(id = request.user.id))
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
    return render(request=request,template_name='registroLavadero.html', context={"lavadero_user_register":lavadero_user_register,"tarifas_lavadero":formulario, "register_lavadero":form, "tiene_lavadero":usuario_tiene_lavadero})


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
    lavadero_user_register = len(Lavadero.objects.filter(id = request.user.id))
    try:
        user = request.user
        lavadero = Lavadero.objects.get(creado_por=user)
        form_n = NewLavaderoFormA()
        TarifaInlineFormset = inlineformset_factory(Lavadero, Tarifa, fields=('tipo', 'monto',), extra=0, can_delete=False, widgets={'tipo':forms.Select(attrs={'readonly':'readonly'})})
        HorarioInlineFormset = inlineformset_factory(Lavadero, Horario, fields=('desde', 'hasta'), extra=0, can_delete=False, widgets={ 'desde':forms.TimeInput(format='%H:%M'), 'hasta':forms.TimeInput(format='%H:%M')})
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
            
        return render(request, 'milavadero.html', {'lavadero_user_register':lavadero_user_register,'form_n':form_n,'tarifa_form':formset_tarifa, 'horario_form':formset_horario, 'estado_form':formset_estado, 'estado':lavadero.get_estado_display})
    else:
        return redirect("registrolavadero")      


@login_required(login_url='/cuentas/login/')
def solicitudLavado(request):
    print("ENTRO A LISTADO DE SOLICITUDES")
    lavadero_user_register = len(Lavadero.objects.filter(id = request.user.id))
    try:
        user = request.user
        lavadero = Lavadero.objects.get(creado_por=user)
    except Lavadero.DoesNotExist:
        lavadero = None

    if lavadero:
        try:
            solicitudes = SolicitudLavadero.objects.filter(lavadero=lavadero, aceptado=None)
            if request.method == "POST":
                id_solicitud = request.POST["id_solicitud"]
                solicitud = SolicitudLavadero.objects.get(pk=id_solicitud)
                cliente = solicitud.cliente
                if 'aceptar' in request.POST:                
                    solicitud.aceptado = True
                    lavadero.estado = 'A'
                    lavadero.save()                                      
                else:
                    print("RECHAZADO")
                    solicitud.aceptado = False
                solicitud.save()
                mailSolicitante(request, cliente, lavadero.creado_por.email, solicitud, lavadero) 
        except SolicitudLavadero.DoesNotExist:
            solicitudes = []
    else:
        return redirect("lavaderos")

    return render(request, 'solicitudLavado.html', {'lavadero_user_register':lavadero_user_register,'solicitudes':solicitudes, 'lavadero':lavadero})


# AGREGAR LOGICA POR CADA BOTON, EN VIEW miLavadero PASAR EL ESTADO ACTUAL DEL LAVADERO COMO CONTEXT PARA PINTAR ESE BOTON DE VERDE
# PUSHEAR A HEROKU PARA ACTIVAR EL TEMA DE VARIABLE DE ENTORNO
@login_required(login_url='/cuentas/login/')
def cambiarEstadoLavadero(request):
    try:
        user = request.user
        lavadero = Lavadero.objects.get(creado_por=user)
    except Lavadero.DoesNotExist:
        lavadero = None

    if lavadero:
        if request.method == "POST":
            if 'setCerrado' in request.POST:
                lavadero.estado = 'C'
                lavadero.save()
                messages.success(request, "Estado cambiado a CERRADO.")
            elif 'setAbierto' in request.POST:
                lavadero.estado = 'A'
                lavadero.save()
                messages.success(request, "Estado cambiado a ABIERTO.")
            elif 'setDisponible' in request.POST:
                lavadero.estado = 'D'
                lavadero.save()
                messages.success(request, "Estado cambiado a DISPONIBLE.")
    
        return redirect("milavadero")   

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
        messages.success(request, f'Bienvenido {user}, dirijase a su bandeja de entrada: {to_email} y presione el boton confirmar cuenta ')
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

# MAIL PARA EL DUEÑO
def mailDueño(request, dueño_lavadero, to_email, cliente, solicitud):
    mail_subject = 'Solicitud de turno de cliente'
    message = render_to_string('template_solicitud_para_dueño.html', {
        'dueño_lavadero': dueño_lavadero,
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': get_current_site(request).domain,
        'cliente': cliente,
        'solicitud': solicitud
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(request, f'Se ha enviado una notificación con la solicitud de lavado.')
    else:
        messages.error(request, f'Ha ocurrido un error enviado un mail a {to_email}')

# MAIL PARA EL CLIENTE SOLICITANTE DE LAVADO
def mailSolicitante(request, cliente, to_email, solicitud, lavadero):
    mail_subject = f'Ha recibido una respuesta de {lavadero.nombre}'
    if solicitud.aceptado:
        estado = "ACEPTADA"
    else:
        estado = "RECHAZADA"
    message = render_to_string('template_respuesta_solicitud.html', {
        'cliente': cliente,
        'domain': get_current_site(request).domain,
        'protocol': 'https' if request.is_secure() else 'http',
        'lavadero': lavadero,
        'solicitud': solicitud,
        'estado' : estado
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    if email.send():
        messages.success(request, f'Se ha enviado una notificación al cliente con la decisión.')
    else:
        messages.error(request, f'Ha ocurrido un error enviado un mail a {to_email}')
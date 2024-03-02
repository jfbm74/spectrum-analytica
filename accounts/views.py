from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

#verification email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# verificacion Whatsapp y SMS
from notifications.views import ws_test, sms_test
import re

# Create your views here.

def register(request):
    """
    Vista para el registro de usuarios.

    Esta vista maneja el proceso de registro de nuevos usuarios en el sistema.
    Si se realiza una solicitud POST válida, se crea un nuevo usuario en la base
    de datos utilizando el formulario de registro. Luego se envía un correo de
    verificación y se redirige al usuario a la página de inicio de sesión.

    """
    # Vista para el registro de usuarios
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():            
            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name']  
            email           = form.cleaned_data['email']
            username        = email.split("@")[0]
            phone_number    = form.cleaned_data['phone_number']
            gov_type_id     = form.cleaned_data['gov_type_id']
            gov_id          = form.cleaned_data['gov_id']
            password        = form.cleaned_data['password']
            # Crear el nuevo usuario
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, phone_number=phone_number, gov_type_id=gov_type_id, gov_id=gov_id, password=password)
            user.phone_number = '+57'+ phone_number
            user.save()

            # User activation by email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
           
            # Extracción de la URL de verificación del mensaje de whatsapp
            match = re.search(r'http://[^\s]+', message)
            if match:
                validation_url = str(match.group())
                print('URL encontrada:', validation_url)
                # Envío de la URL de verificación a través de WhatsApp
                send_ws = sms_test(validation_url, user.phone_number)
            else:
                print('No se encontró ninguna URL en el mensaje.')
            
            # messages.success(request, 'Gracias por registrarte con nosotros. Hemos enviado un correo de verificación a tu cuenta de correo. Por favor verifica')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    """
    Vista para el inicio de sesión de usuarios.

    Esta vista maneja el proceso de inicio de sesión de los usuarios. Si se realiza
    una solicitud POST válida con las credenciales correctas, el usuario es autenticado
    y redirigido a la página de inicio.

    Si se realiza una solicitud GET o una solicitud POST inválida, se muestra el formulario
    de inicio de sesión para que el usuario pueda ingresar sus credenciales.

    """
    # Vista para el inicio de sesión de usuarios
    if request.method == 'POST':
        # Obtener las credenciales del formulario de inicio de sesión
        email = request.POST['email']
        password = request.POST['password']
        # current_location = request.POST['location']

        # Guardar la ubicación en la sesión
        # request.session['current_location'] = current_location
        
        # Autenticar al usuario
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # Iniciar sesión y redirigir al usuario a la página de inicio
            auth.login(request, user)
            # messages.success(request, 'Te encuentras logueado')
            return redirect('home')
        else:
            # Mostrar un mensaje de error si las credenciales son inválidas
            messages.error(request, 'Usuario o contraseña invalidos')
            return redirect('login')
    # Mostrar el formulario de inicio de sesión
    return render(request, 'accounts/login.html')


@login_required(login_url =  'login')
def logout(request):
    """
    Vista para cerrar sesión de usuarios.

    Esta vista maneja el proceso de cierre de sesión de los usuarios. Cuando se realiza
    una solicitud GET, se cierra la sesión del usuario y se muestra un mensaje de éxito.
    Luego, el usuario es redirigido a la página de inicio de sesión.

    """

    # Vista para cerrar sesión de usuarios
    # del request.session['current_location']
    auth.logout(request)
    
    messages.success(request, 'Haz cerrado la sesión exitosamente')
    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    """
    Vista para activar la cuenta de usuario.

    Esta vista maneja el proceso de activación de la cuenta de usuario mediante
    el enlace de verificación. El enlace de verificación contiene un identificador
    de usuario (uidb64) y un token de verificación. Si los valores proporcionados
    son válidos y coinciden, la cuenta de usuario se activa y se muestra un mensaje
    de éxito. Luego, el usuario es redirigido a la página de inicio de sesión.

    Si los valores proporcionados no son válidos o no coinciden, se muestra un
    mensaje de error y se redirige al usuario a la página de registro.

    """
    try:
        # Decodificar el uidb64 y obtener el usuario correspondiente
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
         # Activar la cuenta de usuario
        user.is_active = True
        user.save()
        # Mostrar un mensaje de éxito
        messages.success(request, 'Felicitaciones! Tu cuenta ha sido verificada y se encuentra activa.')
        # Redirigir al usuario a la página de inicio de sesión
        return redirect('login')
    else:
        # Mostrar un mensaje de error si el enlace de verificación es inválido
        messages.error(request, 'Link de verificación fallido')
        # Redirigir al usuario a la página de registro
        return redirect('register')
    
def users(request):
    users_list = Account.objects.all()
    # print(users_list)
    context={
        'users' : users_list
    }
    return render(request, 'accounts/users/user_manager.html', context)

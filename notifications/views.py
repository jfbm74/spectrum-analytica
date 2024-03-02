from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from twilio.rest import Client

def ws_test(message_to_send, phone_number):
    """
    Vista para enviar un mensaje de WhatsApp.

    Esta vista se encarga de enviar un mensaje de WhatsApp a un número de teléfono
    especificado. El mensaje se compone concatenando la variable `message_to_send`
    con un mensaje de saludo.

    Parámetros:
    - message_to_send: El contenido del mensaje a enviar.
    - phone_number: El número de teléfono al que se enviará el mensaje.

    """
    account_sid = 'AC98bd1d751d3ca8e384b72efa5923b704'
    auth_token = '1ec0692411148ec0ae5f02e882f61ac5'
    client = Client(account_sid, auth_token)
    print(phone_number)
    body = 'Hola, tu link de verificación es: ' + message_to_send
    print(body)

    message = client.messages.create(   to='whatsapp:+573117846413',
                                        from_='whatsapp:+14155238886',
                                        body=body
    )
    

def sms_test(message_to_send, phone_number):
    """
    Vista de prueba para enviar un mensaje SMS.

    Esta vista se utiliza para enviar un mensaje SMS de prueba utilizando Twilio.
    Se utiliza una cuenta y un token de autenticación de Twilio para enviar el mensaje.

    """

    print(message_to_send)
    print(phone_number)
    account_sid = 'AC98bd1d751d3ca8e384b72efa5923b704'
    auth_token = '1ec0692411148ec0ae5f02e882f61ac5'
    client = Client(account_sid, auth_token)
    body = 'Por favor haz clic en el enlace de abajo para confirmar tu registro. '+ message_to_send

    message = client.messages.create(
    from_='+14065057276',
    body=body,
    to='+573117846413'
    )

    print(message.sid)

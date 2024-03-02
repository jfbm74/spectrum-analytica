from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    """
        Formulario de registro de usuario.

        Este formulario se utiliza para registrar nuevos usuarios en el sistema.
        Hereda de forms.ModelForm, lo que facilita la creación del formulario
        basado en el modelo de datos Account.

        Atributos:
            - password: Campo de contraseña para el usuario.
            - confirm_password: Campo para confirmar la contraseña.
        
        Métodos:
            - __init__: Inicializa la instancia del formulario y establece atributos personalizados.
            - clean: Realiza la validación personalizada del formulario.

        """
# Definición de los campos de contraseña con widgets personalizados
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese una contraseña', 
        'class': "form-control",
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme la contraseña'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese sus nombres',
        'pattern': '[A-Za-z]+'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese sus Apellidos',
        'pattern': '[A-Za-z]+'
    }))

    gov_id  = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su número de identificación',
        'pattern': '[0-9]+'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su número de identificación',
        'pattern': '[0-9]+'
    }))

    

    class Meta:
        model   = Account
        fields  = ['email', 'first_name', 'last_name', 'phone_number', 'gov_id', 'gov_type_id', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Establecer atributos de clase para todos los campos
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control'

    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        # Validación de contraseñas coincidentes
        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas no coinciden!"
            )
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Clase personalizada de administrador de cuenta
class MyAccountManager(BaseUserManager):
    # Método para crear un usuario
    def create_user(self, first_name, last_name, username, email, phone_number, gov_id, gov_type_id, password=None):
        # Validaciones de campos requeridos
        if not email:
            raise ValueError('El usuario debe tener una dirección de correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        if not phone_number:
            raise ValueError('El usuario debe tener un número de teléfono válido')
        if not gov_id:
            raise ValueError('El usuario debe tener un número de identificación válido')
        if not gov_type_id:
            raise ValueError('El usuario debe tener un tipo de identificación válido')
        
        # Crear instancia de usuario
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number, 
            gov_id=gov_id,
            gov_type_id=gov_type_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Método para crear un superusuario
    def create_superuser(self, first_name, last_name, username, email, phone_number, gov_id, gov_type_id, password):
        # Crear usuario normal usando el método create_user
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number, 
            gov_id=gov_id,
            gov_type_id=gov_type_id,
            password=password,
        )
        
        # Establecer atributos especiales para el superusuario
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


# Modelo de cuenta personalizada que hereda de AbstractBaseUser
class Account(AbstractBaseUser):
    # Opciones para el campo gov_type_id
    GOVERMENT_TYPE_ID_CHOICES = [
        ("CC", "Cedula Ciudadania"),
        ("CE", "Cedula Extranjeria"),
        ("PA", "Pasaporte"),
    ]
    # Campos de la cuenta
    first_name = models.CharField(max_length=50)  # Nombre
    last_name = models.CharField(max_length=50)  # Apellido
    username = models.CharField(max_length=50, unique=True)  # Nombre de usuario
    email = models.EmailField(max_length=100, unique=True)  # Correo electrónico
    phone_number = models.CharField(max_length=50)  # Número de teléfono
    gov_type_id = models.CharField(max_length=20, choices=GOVERMENT_TYPE_ID_CHOICES, default='CC')  # Tipo Identificación gubernamental
    gov_id = models.CharField(max_length=20, unique=True)  # Identificación gubernamental

    # Campos requeridos
    date_joined = models.DateTimeField(auto_now=True)  # Fecha de registro
    last_login = models.DateTimeField(auto_now=True)  # Último inicio de sesión
    is_admin = models.BooleanField(default=False)  # Es administrador
    is_staff = models.BooleanField(default=False)  # Es personal de staff
    is_active = models.BooleanField(default=False)  # Está activo
    is_superadmin = models.BooleanField(default=False)  # Es superadministrador

    # Campo de nombre de usuario para inicio de sesión
    USERNAME_FIELD = 'email'
    # Campos requeridos para crear una cuenta
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number', 'gov_id', 'gov_type_id']

    objects = MyAccountManager()

    def full_name(self):
        # Método para obtener el nombre completo
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        # Representación en cadena de la cuenta (correo electrónico)
        return self.email

    def has_perm(self, perm, obj=None):
        # Método para verificar permisos
        return self.is_admin

    def has_module_perms(self, add_label):
        # Método para verificar permisos del módulo
        return True

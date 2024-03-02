from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.html import format_html

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = (
        'email', 'gov_type_id', 'gov_id', 'first_name', 'last_name', 'username',
        'phone_number', 'gov_type_id', 'gov_id', 'last_login', 'date_joined', 'is_active'
    )  # Campos que se mostrarán en la lista de usuarios en el panel de administración

    list_display_links = ('email', 'first_name', 'last_name')  # Campos enlazados a la vista de detalles de usuario

    readonly_fields = ('last_login', 'date_joined')  # Campos solo de lectura en la vista de detalles de usuario

    ordering = ('-date_joined',)  # Orden de visualización de usuarios en la lista

    filter_horizontal = ()  # Campos ManyToMany que se muestran como una interfaz de selección horizontal

    list_filter = ()  # Campos por los que se pueden filtrar los usuarios en la lista

    fieldsets = ()  # Agrupaciones personalizadas de campos en la vista de detalles de usuario

admin.site.register(Account, AccountAdmin)  # Registro del modelo Account con la configuración de AccountAdmin

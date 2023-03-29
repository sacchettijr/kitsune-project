from django.contrib import admin
from usuario.forms import UsuarioCreationForm, UsuarioChangeForm
from django.contrib.auth import admin as auth_admin
from usuario.models import UsuarioModel
from django.contrib import admin


@admin.register(UsuarioModel)
class UsuarioAdmin(auth_admin.UserAdmin):

    model = UsuarioModel
    ordering = ['pk']
    list_display = [
        'pk', 'email', 'nome', 'cpf_cnpj', 'saldo', 'is_staff', 'is_active', 'is_superuser', 'is_anonymous', 'is_trusty'
    ]
    list_display_links = [
        'pk', 'email', 'nome', 'cpf_cnpj',
    ]

    add_form = UsuarioCreationForm
    add_fieldsets = (
        ('Usuário', {
            'fields': {
                'email',
                ('password1', 'password2')
            }
        }),
        ("Informações básicas", {
            "fields": (
                'nome', 'cpf_cnpj',
            ),
        }),
        ("Permissões", {
            "fields": (
                ('is_active', 'is_staff', 'is_superuser',
                 'is_trusty', 'is_anonymous'),
                'groups', 'user_permissions'
            ),
        }),
    )

    form = UsuarioChangeForm
    fieldsets = (
        ("Usuário", {
            "fields": (
                'email', ('password')
            ),
        }),
        ("Informações básicas", {
            "fields": (
                'nome', 'cpf_cnpj', 'foto_perfil'
            ),
        }),
        ("Permissões", {
            "fields": (
                ('is_active', 'is_staff', 'is_superuser',
                 'is_trusty', 'is_anonymous'),
                'groups', 'user_permissions'
            ),
        }),
    )

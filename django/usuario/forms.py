from django.contrib.auth import forms
from usuario.models import UsuarioModel
from django.forms import ModelForm


class UsuarioCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = UsuarioModel
        fields = [
            'email',
            'password1',
            'password2',
            'nome',
            'cpf_cnpj'
        ]


class UsuarioChangeForm(ModelForm):
    class Meta:
        model = UsuarioModel
        fields = [
            'nome',
            'cpf_cnpj'
        ]


class UsuarioSignUpForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = UsuarioModel
        fields = [
            'email',
            'password1',
            'password2',
            'nome',
            'cpf_cnpj',
        ]


class UsuarioUpdateForm(ModelForm):
    class Meta:
        model = UsuarioModel
        fields = [
            'nome',
            'cpf_cnpj',
            'foto_perfil',
        ]

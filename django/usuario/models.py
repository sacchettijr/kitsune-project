from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import EnderecoModel
from django.core.exceptions import ValidationError
from functions.validacao import cpf_ou_cnpj


def validate_cpf_cnpj(value):

    status, texto, documento = cpf_ou_cnpj(value)

    if status:
        return documento
    else:
        raise ValidationError(texto)


class UsuarioManager(BaseUserManager):

    def create_user(self, email, nome, cpf_cnpj, password=None):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cpf_cnpj=cpf_cnpj)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nome, cpf_cnpj, password):
        user = self.create_user(email, nome, cpf_cnpj, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UsuarioModel(AbstractBaseUser, PermissionsMixin):

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf_cnpj']

    email = models.EmailField('E-Mail', unique=True)
    nome = models.CharField('Nome', max_length=255, blank=True, null=True)
    cpf_cnpj = models.CharField(
        'CPF/CNPJ', max_length=18, unique=True, validators=[validate_cpf_cnpj]
    )
    foto_perfil = models.ImageField(
        upload_to='usuario/user_profile/',
        max_length=100,
        null=True,
        blank=True
    )

    saldo = models.DecimalField(
        'Saldo',
        decimal_places=2,
        max_digits=15,
        default=0.0,
        blank=False,
        null=False
    )

    # PERMISSÕES
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    is_superuser = models.BooleanField('Superusuário', default=False)
    is_anonymous = models.BooleanField('Anonimo', default=False)
    is_trusty = models.BooleanField('E-Mail confirmado', default=False)

    class Meta:
        app_label = 'usuario'
        db_table = 'usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email or self.get_short_name()

    def get_full_name(self):
        return str(self.nome)

    def get_short_name(self):
        return str(self.nome).split(" ")[0]

    def email_user(self, subject, message, from_email=None):
        try:
            send_mail(subject, message, from_email, [self.email])
        except Exception as e:
            print('>>> Usuario.models.RetiradaModel__email_user: {}'.format(e))

    def save(self, *args, **kwargs):
        try:
            # Se for um INSERT
            if not self.pk:
                return super().save(*args, **kwargs)

            #   Se for um UPDATE
            else:
                return super().save(*args, **kwargs)
        except Exception as e:
            print('>>> Usuario.models.RetiradaModel__save: {}'.format(e))

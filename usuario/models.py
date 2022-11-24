from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import EnderecoModel


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
    cpf_cnpj = models.CharField('CPF/CNPJ', max_length=18, unique=True)
    foto_perfil = models.ImageField(
        upload_to='media/usuario/user_profile/',
        height_field=models.PositiveIntegerField(),
        width_field=models.PositiveIntegerField(),
        max_length=100,
        null=True,
        blank=True
    )

    # PERMISSÕES
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    is_superuser = models.BooleanField('Superusuário', default=False)
    is_anonymous = models.BooleanField('Anonimo', default=False)
    is_trusty = models.BooleanField('E-Mail confirmado', default=False)

    class Meta:
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
        send_mail(subject, message, from_email, [self.email])


class UsuarioEnderecoModel(EnderecoModel):
    usuario = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE)
    padrao = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Endereço do usuário'
        verbose_name_plural = 'Endereços dos usuários'
        db_table = 'usuario_endereco'

    def __str__(self):
        informacao = 'Usuário: ' + str(
            self.usuario) + ' - Endereço: ' + self.rua + ', nº ' + self.numero + ', ' + self.bairro + ', CEP ' + self.cep
        if self.complemento:
            informacao = informacao + ', ' + self.complemento
        if self.referencia:
            informacao = informacao + ', ' + self.referencia
        return informacao

    def save(self):
        #  SÓ UM ENDEREÇO COMO PADRÃO
        if self.padrao:
            usuarios_enderecos = UsuarioEndereco.objects.filter(
                padrao=True, produto=self.endereco.pk)
            for usuario_endereco in usuarios_enderecos:
                usuario_endereco.padrao = False
                usuario_endereco.save()
        super().save()

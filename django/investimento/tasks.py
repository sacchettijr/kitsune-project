from celery import shared_task
from usuario.models import UsuarioModel


@shared_task()
def mostrar_clientes():
    usuarios = UsuarioModel.objects.all()
    for u in usuarios:
        print('>>> Usuário: {}'.format(u.pk))

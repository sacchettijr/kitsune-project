from django.urls import path
from usuario.views import usuario_perfil, usuario_update, usuario_mudar_senha
from usuario.views import usuario_list_view


urlpatterns = [
    path('perfil/', usuario_perfil, name='perfil'),
    path('usuarios/', usuario_list_view, name='usuario_list'),
    path('alterar-dados/', usuario_update, name='alterar_dados'),
    path('alterar-senha/', usuario_mudar_senha, name='alterar_senha'),
]

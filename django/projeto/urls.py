from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from core.views import index_view
from usuario.views import signup_usuario_view
from publico.views import publico_index_view

router = routers.DefaultRouter()

urlpatterns = [

    #   DJANGO
    path('admin/', admin.site.urls,),

    #   DEBUG
    path('__debug__/', include('debug_toolbar.urls')),

    #   API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #   PUBLICO
    path('', publico_index_view, name='publico_index_view'),

    #   INTERNO
    path('dashboard/', index_view, name='index_interno'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup_usuario_view, name='signup'),

    path('usuario/', include('usuario.urls')),
    path('administracao/', include('usuario.urls')),
    path('investimento/', include('investimento.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

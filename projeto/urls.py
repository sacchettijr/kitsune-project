from django.contrib import admin
from django.urls import path, include
from core.views import index_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', index_view, name='index_interno'),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/cadastro/', usuario_cadastro,
]

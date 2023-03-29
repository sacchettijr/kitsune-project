from django.contrib import admin
from core.models import PaisModel, EstadoModel, CidadeModel


@admin.register(PaisModel)
class PaisAdmin(admin.ModelAdmin):
    pass


@admin.register(EstadoModel)
class EstadoAdmin(admin.ModelAdmin):
    pass


@admin.register(CidadeModel)
class CidadeAdmin(admin.ModelAdmin):
    pass

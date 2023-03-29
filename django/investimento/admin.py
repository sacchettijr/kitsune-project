from django.contrib import admin
from investimento.models import InvestimentoModel, RetiradaModel


@admin.register(InvestimentoModel)
class InvestimentoAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'proprietario',
        'valor_investido',
        'data_investimento',
        'meses_de_investimento',
        'status',
    ]
    fields = ('proprietario', 'valor_investido', 'data_investimento',)


@admin.register(RetiradaModel)
class RetiradaAdmin(admin.ModelAdmin):
    list_display = [
        'pk', 'investimento', 'data_retirada', 'taxa_ganho', 'taxa_tributo', 'imposto', 'lucro_bruto', 'lucro_liquido', 'valor_final_b', 'valor_final_l',
    ]
    list_display_links = ['pk', 'investimento',]
    fields = ('investimento', 'data_retirada',)

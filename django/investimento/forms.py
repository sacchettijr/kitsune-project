from django.forms import ModelForm
from investimento.models import InvestimentoModel, RetiradaModel


class InvestimentoCadastroForm(ModelForm):
    class Meta:
        model = InvestimentoModel
        fields = [
            'valor_investido',
            'data_investimento',
        ]


class RetiradaCadastroForm(ModelForm):
    class Meta:
        model = RetiradaModel
        fields = [
            'investimento',
            'data_retirada',
        ]

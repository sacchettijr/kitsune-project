from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from investimento.models import InvestimentoModel
from functions.investimento import calculo_retirada
from decimal import Decimal


class IndexInternoView(LoginRequiredMixin, TemplateView):
    template_name = 'interno/interno_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['algo'] = 'ALGO'
        try:
            context['total_bruto'] = Decimal(0.00)
            context['total_liquido'] = Decimal(0.00)
            context['lucro_liquido'] = Decimal(0.00)
            context['lucro_bruto'] = Decimal(0.00)

            investimentos = InvestimentoModel.objects.filter(
                proprietario=self.request.user.pk, status=True
            )

            for i in investimentos:

                dados = calculo_retirada(
                    data_investimento=i.data_investimento,
                    valor_investido=i.valor_investido
                )

                context['total_bruto'] = context['total_bruto'] + dados['valor_final_b']
                context['total_liquido'] = context['total_liquido'] + dados['valor_final_l']
                context['lucro_liquido'] = context['lucro_liquido'] + dados['lucro_liquido']
                context['lucro_bruto'] = context['lucro_bruto'] + dados['lucro_bruto']
        except Exception as e:
            print('>>> Erro: {}'.format(e))
        finally:
            return context


index_view = IndexInternoView.as_view()

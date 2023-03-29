
from django.views.generic import CreateView, ListView, DetailView
from investimento.models import InvestimentoModel, RetiradaModel
from django.contrib.auth.mixins import LoginRequiredMixin
from investimento.forms import InvestimentoCadastroForm
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy
from django.http import HttpResponse


class InvestimentoCadastroView(LoginRequiredMixin, CreateView):
    template_name = 'investimento/investimento_cadastro.html'
    model = InvestimentoModel
    form_class = InvestimentoCadastroForm
    success_url = reverse_lazy('investimento_lista')

    def form_valid(self, form):
        try:
            self.object = form.save(commit=False)
            self.object.proprietario_id = self.request.user.pk
            self.object.save()
        except Exception as e:
            print('Erro: {}'.format(e))
        finally:
            return super(InvestimentoCadastroView, self).form_valid(form)


class InvestimentoListaView(LoginRequiredMixin, ListView):
    template_name = 'investimento/investimento_lista.html'
    model = InvestimentoModel

    def get_queryset(self):
        #   Pega o ID do usuário e filtra apenas seus investimentos
        return InvestimentoModel.objects.filter(
            proprietario=self.request.user.pk
        )


class InvestimentoDetalheView(LoginRequiredMixin, DetailView):
    template_name = 'investimento/investimento_detalhe.html'
    model = InvestimentoModel


class RetiradaListaView(LoginRequiredMixin, ListView):
    template_name = 'investimento/investimento_retirada_lista.html'
    model = RetiradaModel

    def get_queryset(self):
        #   Pega o ID do usuário e filtra apenas suas retiradas
        return RetiradaModel.objects.filter(investimento__proprietario=self.request.user.pk)


def retiradaCadastroView(request, investimento):
    context = {}

    try:
        ...
    except:
        ...
    finally:
        ...


def sem_falsos_verdadeiros():
    #   Pega todos os dados que já possuem retirada registrada mas que o status manteve True,
    #   depois faz a alteração do status para False

    try:
        investimentos = InvestimentoModel.objects.filter(status=True).order_by('pk')

        objetos_falhos = RetiradaModel.objects.filter(investimento__in=investimentos)
        for o in objetos_falhos:
            objeto = get_object_or_404(InvestimentoModel, pk=o.investimento.pk)
            objeto.status = False
            objeto.save()
        return HttpResponse(status=200)
    except Exception as e:
        print('>>> investimento.views__treino_task: {}'.format(e))
        return e


investimento_cadastro = InvestimentoCadastroView.as_view()
investimento_lista = InvestimentoListaView.as_view()
investimento_detalhe = InvestimentoDetalheView.as_view()
retirada_lista = RetiradaListaView.as_view()

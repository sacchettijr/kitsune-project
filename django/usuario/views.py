import re
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm
from usuario.forms import UsuarioSignUpForm, UsuarioUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from functions.investimento import calculo_retirada
from usuario.models import UsuarioModel


class UsuarioSignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UsuarioSignUpForm
    model = UsuarioModel
    success_url = reverse_lazy('login')


class UsuarioPerfilView(LoginRequiredMixin, DetailView):
    template_name = 'usuario/usuario_detail.html'
    model = UsuarioModel

    def get_object(self):
        return self.request.user


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'usuario/usuario_update.html'
    model = UsuarioModel
    form_class = UsuarioUpdateForm
    success_url = reverse_lazy('perfil')

    def get_object(self):
        return self.request.user


class UsuarioMudarSenhaView(LoginRequiredMixin, FormView):
    template_name = 'usuario/senha_update.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('perfil')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UsuariosListView(LoginRequiredMixin, ListView):
    template_name = 'administracao/usuarios.html'
    model = UsuarioModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# def calcular_saldos():

#     try:
#         saldo_b, saldo_l = calculo_saldo(
#             InvestimentoModel.objects.filter(
#                 proprietario=usuario,
#                 status=True
#             )
#         )
#     except Exception as e:
#         print('>>> investimento.views__calcular_saldo: {}'.format(e))
#         return e


usuario_list_view = UsuariosListView.as_view()
signup_usuario_view = UsuarioSignUpView.as_view()
usuario_perfil = UsuarioPerfilView.as_view()
usuario_update = UsuarioUpdateView.as_view()
usuario_mudar_senha = UsuarioMudarSenhaView.as_view()

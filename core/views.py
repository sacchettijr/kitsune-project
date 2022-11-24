
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexInternoView(LoginRequiredMixin, TemplateView):
    template_name = 'interno/index.html'


index_view = IndexInternoView.as_view()

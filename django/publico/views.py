from django.shortcuts import render
from django.views.generic import TemplateView


class PublicoIndexView(TemplateView):
    template_name = 'publico/publico_index.html'


publico_index_view = PublicoIndexView.as_view()

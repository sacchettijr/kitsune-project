from django.urls import path, include
from investimento.views import investimento_cadastro, investimento_lista, investimento_detalhe, retirada_lista, sem_falsos_verdadeiros

urlpatterns = [
    #   Investimento
    path('cadastro/', investimento_cadastro, name="investimento_cadastro"),
    path('lista/', investimento_lista, name="investimento_lista"),
    path('detail/<int:pk>/', investimento_detalhe, name="investimento_detalhe"),

    #   Retiradas
    path('retiradas/lista/', retirada_lista, name='retirada_lista'),

    path('treino_task/', sem_falsos_verdadeiros, name="treino_task"),
]

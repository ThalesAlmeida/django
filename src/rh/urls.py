from django.urls import path

from rh.views import Home, PessoaFisicaCreate, PessoaFisicaListView

app_name = 'rh'

urlpatterns = [
    # Servidor
    path('criar_edicao', PessoaFisicaCreate.as_view(), name='atualizacao_create'),
    path('pessoafisicalist/', PessoaFisicaListView.as_view(), name='pessoafisica_list'),
    path('home/', Home.as_view(), name='home'),
]

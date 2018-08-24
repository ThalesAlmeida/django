

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from atualizacao.models import Atualizacao
from contrib.api import AthenasAPI
from rh.models import PessoaFisica, Servidor

from .forms import AtualizacaoForm, PessoaFisicaForm


# Views de Servidor
class Home(ListView):
    model = Atualizacao
    template_name = 'rh/home.html'


class AtualizacaoCreate(CreateView):
    form_class = AtualizacaoForm
    model = Atualizacao
    template_name = 'rh/atualizacao_form.html'

    def get_form(self, *args, **kwargs):
        form = super(AtualizacaoCreate, self).get_form(*args, **kwargs)
        return form


class PessoaFisicaCreate(SuccessMessageMixin, CreateView):
    form_class = PessoaFisicaForm
    model = PessoaFisica
    template_name = 'rh/atualizacao_form.html'
    success_url = reverse_lazy('rh:home')
    success_message = "Atualizado com sucesso"

    def get_form(self, *args, **kwargs):
        if self.request.method == 'GET':
            user_cpf = Servidor.objects.get(user=self.request.user).cpf

            # athenas_user = AthenasAPI.get_pessoa_fisica(user_cpf)
            athenas_user = AthenasAPI.get_pessoa_fisica(user_cpf)
            form = PessoaFisicaForm({
                'nome': athenas_user['nome'],
                'estado_civil': athenas_user['estado_civil'],
                'raca_cor': 'BRANCA',
                'data_nascimento': athenas_user['data_nascimento'],
                'rg': athenas_user['rg'],

                'cpf': athenas_user['cpf'],
                'nome_mae': athenas_user['nome_mae'],
                'nome_pai': athenas_user['nome_pai']
            })
            return form
        else:
            form = PessoaFisicaForm(self.request.POST)
            return form

    def form_valid(self, form):
        pessoa_fisica = PessoaFisica()
        pessoa_fisica = form.save()

        atualizacao = Atualizacao()

        atualizacao.pessoa_fisica = pessoa_fisica
        atualizacao.status = 'AGUARDANDO_VALIDACAO'
        atualizacao.save()

        return super(PessoaFisicaCreate, self).form_valid(form)

    # def form_invalid(self, form):
    #     # raise Exception(form.errors)


class PessoaFisicaListView(ListView):
    model = PessoaFisica

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

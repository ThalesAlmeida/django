from django import forms

from atualizacao.models import Atualizacao
from rh.models import PessoaFisica

# from .const import ESTADO_CIVIL_CHOICES


class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        # exclude = ['endereco']
        fields = ['cpf', 'nome', 'raca_cor', 'estado_civil', 'nome_mae', 'nome_pai']
        # fields = ['nome', 'cpf', 'rg', 'data_nascimento', 'nome_mae', 'nome_pai']


class AtualizacaoForm(forms.ModelForm):
    class Meta:
        model = Atualizacao
        fields = '__all__'

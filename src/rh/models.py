import logging

from django.contrib.auth.models import User
from django.db import models

from rh.const import (DOCUMENTO_CHOICES, ESTADO_CIVIL_CHOICES, FATOR_RH, GRAU_INSTRUCAO_CHOICES, RACA_COR_CHOICES,
                      SANGUE, SEXO_CHOICES, TIPO_CONTA_CHOICES, TIPO_ENDERECO_CHOICES, TIPO_LOGRADOURO_ENDERECO_CHOICES,
                      TIPO_TELEFONE_CHOICES)

log = logging.getLogger(__name__)


class Telefone(models.Model):
    tipo_telefone = models.CharField(max_length=20, choices=TIPO_TELEFONE_CHOICES, verbose_name=u'Tipo de Telefone')
    numero = models.CharField(max_length=15, verbose_name=u'Número')
    publico = models.BooleanField(default=False, verbose_name=u'Público')
    data_alteracao = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Telefone'

    def __str__(self):
        return self.numero


class Endereco(models.Model):
    tipo_endereco = models.CharField(max_length=20, choices=TIPO_ENDERECO_CHOICES, verbose_name=u'Tipo do Endereço')
    tipo_logradouro = models.CharField(max_length=20, choices=TIPO_LOGRADOURO_ENDERECO_CHOICES, verbose_name='Tipo do Logradouro')
    municipio = models.ForeignKey('Localidade', null=True, blank=False, on_delete=True)
    cep = models.CharField(max_length=10, verbose_name='CEP', null=True, blank=False)
    logradouro = models.CharField(max_length=100, null=True, blank=False)
    numero = models.CharField(max_length=12, blank=True, null=True, verbose_name=u'Número')
    bairro = models.CharField(max_length=50, null=True, blank=True)
    complemento = models.CharField(max_length=2000, blank=True, null=True)
    data_alteracao = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Endereço'

    def __str__(self):
        return 'Endereço : {} {}'.format(self.tipo_endereco, self.cep)


class DadoBancario(models.Model):
    banco = models.ForeignKey('Banco', on_delete=True)
    tipo_conta = models.IntegerField(choices=TIPO_CONTA_CHOICES, verbose_name=u'Tipo de Conta')
    agencia = models.CharField(max_length=15, verbose_name=u'Agência com DV')
    conta_corrente_completa = models.CharField(max_length=15, verbose_name='Conta Corrente com DV')

    def __str__(self):
        return u"{banco} - {tipo} - Ag: {agencia} - Número: {numero}".format(
            banco=(self.banco),
            tipo=(self.tipo_conta),
            agencia=self.agencia,
            numero=self.conta_corrente_completa
        )

    def _validate(self):
        return True

    def validate(self):
        if hasattr(self, '_validate%s' % self.banco.numero):
            getattr(self, '_validate%s' % self.banco.numero)()
        else:
            self._validate()

    class Meta:
        verbose_name = u'Dado Bancário'

    class ValidateAgencia(Exception):
        def __init__(self):
            Exception.__init__('Número de agência inválido!')

    class ValidateConta(Exception):
        def __init__(self):
            Exception.__init__('Número de conta bancária inválido!')


class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name=u'Nome')
    endereco = models.ForeignKey('Endereco', null=True, blank=True, verbose_name=u'Endereço', on_delete=True)
    telefone = models.ForeignKey('Telefone', null=True, blank=True, on_delete=True)
    dado_bancario = models.ForeignKey('DadoBancario', null=True, blank=True, verbose_name=u'Dado Bancário', related_name='dados_bancarios_pessoas', on_delete=True)
    # data_alteracao = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = u'Pessoa'
        # ordering = ('nome')


class Estado(models.Model):
    pais = models.ForeignKey('Pais', verbose_name=u'País', on_delete=True)
    sigla = models.CharField(max_length=2)
    siafi = models.CharField(max_length=12, null=True, blank=True, verbose_name=u'SIAFI')
    tse = models.CharField(max_length=12, null=True, blank=True, verbose_name=u'TSE')
    ibge = models.IntegerField(verbose_name=u'IBGE', null=True, blank=True)

    class Meta:
        verbose_name = 'Estado'

    def __str__(self):
        return 'Estado: {} {} '.format(self.nome, self.sigla)


class Documento(models.Model):
    tipo_documento = models.IntegerField(choices=DOCUMENTO_CHOICES, verbose_name=u'Tipo de Documento')
    numero = models.CharField(max_length=30, verbose_name='Número')
    data_expedicao = models.DateField(verbose_name=u'Data da Expedição', null=True, blank=True)
    data_validade = models.DateField(verbose_name=u'Data de Validade', null=True, blank=True)
    estado_expedicao = models.ForeignKey(Estado, verbose_name=u'Estado de Expedição', null=True, blank=True, on_delete=True)

    class Meta:
        verbose_name = u'Documento'

    def __str__(self):
        return 'Documento : {} - {}'.format(self.tipo_documento, self.numero)


# class MesoRegiao(CObject):
#     passPessoa

#     class Meta:
#         verbose_name = 'Meso Região'

#     def __str__(self):
#         return self.nome

class Municipio(models.Model):
    estado = models.ForeignKey('Estado', on_delete=True)
    sigla = models.CharField(max_length=6, null=True, blank=True)
    siafi = models.CharField(max_length=12, null=True, blank=True)
    ibge = models.IntegerField(null=True, blank=True, verbose_name=u'IBGE')
    valor_vale_transporte = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=u'Valor vale transporte')

    class Meta:
        verbose_name = 'Município'

    def __int__(self):
        return self.estado


class Localidade(Municipio):
    cep = models.CharField(max_length=9, null=True, blank=True)
    distancia_capital = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=u'Distância Capital')
    indicador_municipio = models.BooleanField(default=False, verbose_name=u'Indicador Município', blank=True)
    sede_termo = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = 'Localidade'

    def __int__(self):
        return self.microregiao


class NecessidadeEspecial(models.Model):
    def __str__(self):
        return (self.nome)


class PessoaFisicaNecessidadeEspecial(models.Model):
    pessoafisica = models.ForeignKey('PessoaFisica', verbose_name=u'Servidor', related_name='necessidades_pessoa', on_delete=True)
    necessidadeespecial = models.ForeignKey('NecessidadeEspecial', null=True, blank=True, verbose_name=u'Necessidade Especial', related_name='pessoas_necessidade', on_delete=True)
    observacao = models.TextField(null=True, blank=True, verbose_name=u'Observação')

    class Meta:
        db_table = u'rh_pessoafisica_necessidades_especiais'

    def __str__(self):
        return u"{} - {}".format(self.pessoafisica.nome, self.necessidadeespecial)


class Servidor(models.Model):
    user = models.OneToOneField(User, related_name='servidor', on_delete=True)
    cpf = models.CharField(max_length=14, null=True, blank=True, verbose_name='CPF')

    def __str__(self):
        return self.cpf


class PessoaFisica(Pessoa):
    servidor = models.OneToOneField(Servidor, blank=True, null=True, on_delete=models.PROTECT, related_name='servidor', verbose_name='servidor')
    cpf = models.CharField(max_length=14, null=True, blank=True, verbose_name=u'CPF')
    rg = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'RG')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
    sangue = models.CharField(choices=SANGUE, max_length=40, blank=True, default='INDEFINIDO')
    documento = models.ForeignKey('Documento', null=True, blank=True, on_delete=True)
    estado_civil = models.CharField(max_length=40, choices=ESTADO_CIVIL_CHOICES, default='NAO DEFINIDO NO CADASTRO')
    municipio_naturalidade = models.ForeignKey('Localidade', null=True, blank=True, on_delete=True)
    raca_cor = models.CharField(max_length=20, choices=RACA_COR_CHOICES, verbose_name=u'Raça/Cor')
    email_pessoal = models.EmailField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    data_obito = models.DateField(null=True, blank=True, verbose_name=u'Data Óbito')
    rg_orgao = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'RG Órgão')
    rg_data_expedicao = models.DateField(null=True, blank=True, verbose_name=u'RG Data Expedição')
    rg_uf = models.ForeignKey('Estado', null=True, blank=True, verbose_name=u'RG UF', on_delete=True)
    fator_rh = models.CharField(max_length=10, choices=FATOR_RH, null=True, blank=True, verbose_name=u'Fator RH')
    doador = models.BooleanField(default=True, blank=True, verbose_name=u'Doador de órgãos')
    nome_pai = models.CharField(max_length=80, null=True, blank=True, verbose_name=u'Nome Pai')
    nome_mae = models.CharField(max_length=80, null=True, blank=True, verbose_name=u'Nome Mãe')
    nome_conjuge = models.CharField(max_length=80, null=True, blank=True, verbose_name=u'Nome Cônjuge')
    necessidade_especial = models.BooleanField(default=False, blank=True, verbose_name=u'Necessidade Especial')
    necessidades_especiais = models.ForeignKey('NecessidadeEspecial', null=True, blank=True, on_delete=True)
    grau_instrucao = models.CharField(max_length=40, choices=GRAU_INSTRUCAO_CHOICES, null=True, blank=True)
    possui_filhos = models.BooleanField(default=False, blank=True, verbose_name=u'Possui filhos')
    ativo = models.BooleanField(default=True, verbose_name='ativo')

    class Meta:
        verbose_name = 'Pessoa Física'
        ordering = ("nome", "cpf")

    def __str__(self):
        return self.nome

from django.db import models
from django.db.models import Manager

from standard.models import AuditTimestampModel, CObject

# from model_utils.managers import PassThroughManager

# from contrib.decorator import to_search


class Pais(CObject):
    codigo = models.CharField(max_length=12, verbose_name='DDI', null=True)
    nome_completo = models.CharField(max_length=100, null=True)
    nacionalidade = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'País'


class Circunscricao(CObject):
    pass


class GrupoComarca(CObject):
    pass


class MesoRegiao(CObject):
    pass


class TipoOrigem(CObject):
    pass


# PassThroughManager
class TopicManager(Manager):
    pass


class Entrancia(CObject):
    class Meta:
        ordering = ['nome']


class Instancia(CObject):
    class Meta:
        ordering = ['nome']


class Capacidade(CObject):
    pass


class InCapacidade(CObject):
    pass


class Cbo(AuditTimestampModel):
    codigo = models.CharField(max_length=10, verbose_name=u'Código')
    descricao = models.CharField(max_length=250, verbose_name=u'Descrição')

    def __unicode__(self):
        return (self.codigo + ' - ' + self.descricao)


class Especialidade(CObject):
    sigla = models.CharField(max_length=3, null=True)

    class Meta:
        ordering = ['nome']


class Banco(CObject):
    numero = models.CharField(max_length=3, verbose_name=u'Número', unique=True)
    sigla = models.CharField(max_length=6, null=True)
    tem_convenio = models.PositiveIntegerField(
        choices=(
            (0, u"NÃO"),
            (1, u"SIM"),
            (2, u"DOCUMENTO ELETRÔNICO DE CRÉDITO (DOC)"),
        ),
        null=True,
        verbose_name=u'Tem Convênio?'
    )
    numero_convenio = models.CharField(max_length=20, null=True, verbose_name=u'Número Convênio')
    agencia = models.CharField(max_length=10, null=True, verbose_name=u'Agência')
    dv_agencia = models.CharField(max_length=2, null=True, verbose_name=u'DV Agência')
    conta = models.CharField(max_length=20, null=True)
    dv_conta = models.CharField(max_length=2, null=True, verbose_name=u'DV Conta')
    principal = models.BooleanField(default=False, verbose_name=u'Banco Principal')
    sequencial_arquivo = models.IntegerField(verbose_name=u'Sequencial', null=False, default=0)

    class Meta:
        # ordering = ['nome']
        verbose_name = 'Banco'

    def save(self, force_insert=False, force_update=False):
        if self.tem_convenio == 1 and (self.numero_convenio is None or self.agencia is None or self.conta is None):
            raise Exception(u"As informações do convênio não estão preenchidas!")
        if self.principal == 1:
            if self.tem_convenio != 1:
                raise Exception(u"Um banco sem convênio não pode ser marcado como principal!")
        super(Banco, self).save(force_insert, force_update)

    def __unicode__(self):
        return u"%s - %s" % (self.numero, self.nome)

    def _get_conta_completa(self):
        return "%s%s" % (self.conta, self.dv_conta)
    conta_completa = property(_get_conta_completa)

    def get_sequencial(self):
        self.sequencial_arquivo = (self.sequencial_arquivo + 1) if self.sequencial_arquivo < 999999 else 1
        self.save()
        return self.sequencial_arquivo

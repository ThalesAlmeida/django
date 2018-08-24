# from django.conf import settings
from django.db import models

from rh.const import DOCUMENTO_CHOICES
from rh.models import PessoaFisica

from .consts import ATUALIZACAO_STATUS


class Comprovante(models.Model):
    tipo = models.SmallIntegerField(choices=DOCUMENTO_CHOICES, null=True)
    # document = models.FileField(upload_to=settings.MEDIA_ROOT, verbose_name='documento', null=True, blank=True)


class Atualizacao(models.Model):
    status = models.CharField(max_length=50, choices=ATUALIZACAO_STATUS)
    criacao_data = models.DateTimeField(auto_now_add=True)
    envio_data = models.DateTimeField(auto_now_add=True)
    # tipo_comprovante = models.ManyToManyField(Comprovante, blank=True)
    pessoa_fisica = models.OneToOneField(PessoaFisica, on_delete=models.CASCADE)

    def __str__(self):
        return self.status

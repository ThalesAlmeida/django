from django.contrib import admin

from atualizacao.models import Atualizacao, Comprovante

from .models import (DadoBancario, Documento, Endereco, Estado, Localidade, Municipio, NecessidadeEspecial, Pessoa,
                     PessoaFisica, Telefone)
from .parametros import (Banco, Capacidade, Circunscricao, Entrancia, GrupoComarca, InCapacidade, Instancia, MesoRegiao,
                         Pais, TipoOrigem)

# Register your models here. O

admin.site.register(Pessoa)
admin.site.register(PessoaFisica)
admin.site.register(Telefone)
admin.site.register(Endereco)
admin.site.register(Pais)
admin.site.register(Documento)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(DadoBancario)
admin.site.register(Localidade)
admin.site.register(Banco)
admin.site.register(MesoRegiao)
admin.site.register(GrupoComarca)
admin.site.register(Circunscricao)
admin.site.register(Entrancia)
admin.site.register(Instancia)
admin.site.register(Capacidade)
admin.site.register(InCapacidade)
admin.site.register(TipoOrigem)
admin.site.register(NecessidadeEspecial)
admin.site.register(Atualizacao)
admin.site.register(Comprovante)

import logging

from django.db import transaction

import requests
from decouple import config

from contrib.exceptions import RecadastramentoException
from rh.models import PessoaFisica

logger = logging.getLogger(__name__)


class APIException(RecadastramentoException):
    pass


class AthenasAPI(object):

    ATHENAS_URL = config(
        'ATHENAS_URL',
        default='https://athenas.defensoria.to.def.br/athenas')

    ATHENAS_API_GET_PESSOAFISICA = '{}/api/pessoafisica/{}'.format(
        ATHENAS_URL, '?ativo=True')

    @classmethod
    @transaction.atomic
    def get_pessoa_fisica_(cls, cpf):
        response = requests.get(cls.ATHENAS_API_GET_PESSOAFISICA, params={'cpf': cpf}).json()

        if response.get('count') == 1:
            api_pessoa_fisica = response['results'][0]

            pessoa, created = PessoaFisica.objects.update_or_create(
                cpf=api_pessoa_fisica['cpf'],
                defaults={
                    'nome': api_pessoa_fisica['nome'],
                    'ativo': True,
                    'data_nascimento': api_pessoa_fisica['data_nascimento'],
                    'rg': api_pessoa_fisica['rg'],
                    'nome_mae': api_pessoa_fisica['nome_mae'],
                    'nome_pai': api_pessoa_fisica['nome_pai'],
                    # 'raca_cor': api_pessoa_fisica['raca_cor'],
                    # 'telefone': api_pessoa_fisica['telefones'],
                }
            )

            # if 'telefones' in api_pessoa_fisica and len(api_pessoa_fisica['telefones']) > 0:
            #     for api_telefone in api_pessoa_fisica['telefones']:
            #         Telefone.objects.create(
            #             numero=api_telefone['numero'],
            #             publico=api_telefone['publico'],
            #             tipo_telefone=TipoTelefone.RESIDENCIAL
            #         )

            return pessoa

        else:
            raise APIException('Pessoa física com cpf ' '{}' ' não encontrada no Athenas.'.format(cpf))

    @classmethod
    def get_pessoa_fisica(cls, cpf):
        response = requests.get(cls.ATHENAS_API_GET_PESSOAFISICA, params={'cpf': cpf}).json()
        return response['results'][0]

    # @staticmethod
    # def get_servidor_from_api(api_servidor):
    #     """
    #     Cria ou atualiza uma instância de Servidor a partir de um objeto
    #     Servidor JSON da API.

    #     Args:
    #         api_servidor (dict): JSON contendo os dados do servidor passados
    #         pela API.

    #     Returns:
    #         tuple (Servidor, bool): Tupla contendo o servidor criado ou
    #         atualizado e um booleano True caso tenha sido criado um novo
    #         registro ou False caso contrário.

    #     """

    #     keys = ['cpf', 'nome', 'ativo', 'matricula', 'servidor_lotacao']

    #     if not all(k in api_servidor.keys() for k in keys) \
    #             and api_servidor.get('cpf'):

    #         response = requests.get(
    #             settings.ATHENAS_API_GET_SERVIDOR_BY_CPF %
    #             api_servidor.get('cpf')).json()

    #         if response.get('count') == 1:
    #             api_servidor = response['results'][0]

    #     return Servidor.objects.update_or_create(
    #         cpf=api_servidor['cpf'],
    #         defaults={
    #             'nome': api_servidor['nome'],
    #             'ativo': api_servidor['ativo'],
    #             'matricula': api_servidor['matricula'],
    #             'lotacao': AthenasAPI.get_lotacao_from_api_servidor(
    #                 api_servidor)[0]
    #         }
    #     )

    # @staticmethod
    # def _recupera_lotacao_ativa(api_servidor):
    #     servidor_lotacao_list = api_servidor['servidor_lotacao']
    #     servidor_lotacao_ativas_list = []

    #     for servidor_lotacao in servidor_lotacao_list:
    #         if servidor_lotacao['ativo']:
    #             servidor_lotacao_ativas_list.append(servidor_lotacao)

    #     # retorna None caso não haja lotações ativas
    #     if not servidor_lotacao_ativas_list:
    #         logger.warning(
    #             'Servidor "%s" não possui lotação ativa',
    #             api_servidor['matricula'])

    #         return None

    #     # retorna a única lotação ativa
    #     elif len(servidor_lotacao_ativas_list) == 1:
    #         return servidor_lotacao_ativas_list[0]['lotacao']

    #     # busca por designação caso haja mais de uma lotação ativa
    #     elif len(servidor_lotacao_ativas_list) > 1:
    #         for servidor_lotacao in servidor_lotacao_ativas_list:
    #             if servidor_lotacao['designacao']:
    #                 return servidor_lotacao['lotacao']

    #         # busca por lotações não acumuladas caso não encontre designação
    #         for servidor_lotacao in servidor_lotacao_ativas_list:
    #             if not servidor_lotacao['acumulacao']:
    #                 return servidor_lotacao['lotacao']

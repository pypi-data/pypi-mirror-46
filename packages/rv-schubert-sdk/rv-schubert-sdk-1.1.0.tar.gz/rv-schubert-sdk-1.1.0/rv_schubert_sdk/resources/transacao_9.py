"""
Transação 9 - Consulta Limite de Credito
"""
from decimal import Decimal

from .exceptions import ErroRV
from .rv_api import RVapi


class Transacao9(RVapi):
    LIMITE_CREDITO = None
    LIMITE_DISPONIVEL = None
    ANTECIPADO = None
    VALOR_ABERTO = None

    def execute(self, mock = None):
        if mock is None:
            payload = {
                "codigo_transacao": 9,
                "loja_primaria": self.CREDENCIAIS['loja_primaria'],
                "nome_primario": self.CREDENCIAIS['nome_primario'],
                "senha_primaria": self.CREDENCIAIS['senha_primaria'],
                "versao": self.VERSAO,
            }

            response = self.doPOST(payload)
        else:
            response = mock

        response = self.convert_xml_to_dict(response)

        try:
            self.LIMITE_CREDITO = Decimal(response.get('cellcard').get('limite_credito'))
            self.LIMITE_DISPONIVEL = Decimal(response.get('cellcard').get('limite_disponivel'))
            self.ANTECIPADO = Decimal(response.get('cellcard').get('antecipado'))
            self.VALOR_ABERTO = Decimal(response.get('cellcard').get('valor_aberto'))
        except:
            raise ErroRV("Não foi possível consultar os limites de crédito")

        return response

"""
Transação 7 - Confirmação / Desfazimento de Transações
"""
from decimal import Decimal

from .exceptions import ErroRV
from .rv_api import RVapi


class Transacao7(RVapi):
    CONFIRMADO = False
    CANCELADO = False

    def execute(self, compra: int, cod_retorno: int = 0, mock=None) -> dict:
        """
        :param compra: Codigo da compra no sistema do cliente
        :param cod_retorno: 0 - Confirmar Transacao | 1 - Cancelar Transacao
        :param mock: Bypass no server para testes
        :return: dict
        """
        if mock is None:
            payload = {
                "codigo_transacao": 7,
                "loja_primaria": self.CREDENCIAIS['loja_primaria'],
                "nome_primario": self.CREDENCIAIS['nome_primario'],
                "senha_primaria": self.CREDENCIAIS['senha_primaria'],
                "versao": self.VERSAO,
                "compra": compra,
                "cod_retorno": cod_retorno
            }

            response = self.doPOST(payload)
        else:
            response = mock

        response = self.convert_xml_to_dict(response)

        try:
            self.CONFIRMADO = True if response.get('cellcard').get('cod_retorno') == '0' else False
            self.CANCELADO =True if response.get('cellcard').get('cod_retorno') == '1' else False
        except:
            ErroRV('Não foi possivel definir o status da transação')

        return response

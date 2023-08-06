"""
Transação 5 - Venda de recarga online
"""
from decimal import Decimal

from .rv_api import RVapi
from .objetos.recarga import Recarga


class Transacao5(RVapi):

    def execute(
            self,
            compra: int,
            produto: str,
            ddd: str,
            fone: str,
            codigo_assinante: str = None,
            valor: Decimal = None,
            id_terminal: str = None,
            bit_boleto: int = None,
            usuario_local: str = None,
            mock=None
    ) -> Recarga:
        """
        Parametros
        :param compra: Codigo da compra no sistema do cliente, sequencial unico com maximo de 9 digitos
        :param produto: Codigo do produto consultado na Transacao1
        :param ddd: DDD se recarga de telefone
        :param fone: Telefone do cliente se recarga de telefone com 8 ou 9 digitos
        :param codigo_assinante: Codigo do assintante para venda de produtos TV
        :param valor: Valor da recarga para produtos que aceitem configuracao
        :param id_terminal: Codigo do terminal que esta realizando a venda
        :param bit_boleto: Informar se houver boletos em aberto
        :param usuario_local: Codigo ou Login do cliente local se houver para relatorio de compras
        :param mock:
        :return:
        """
        if mock is not None:
            response = mock
        else:
            payload = {
                "codigo_transacao": 3,
                "loja_primaria": self.CREDENCIAIS['loja_primaria'],
                "nome_primario": self.CREDENCIAIS['nome_primario'],
                "senha_primaria": self.CREDENCIAIS['senha_primaria'],
                "versao": self.VERSAO,
                "compra": compra,
                "produto": produto,
                "ddd": ddd,
                "fone": fone,
                "codigoAssinante": codigo_assinante,
            }

            if valor is not None:
                payload['valor'] = valor

            if id_terminal is not None:
                payload['id_terminal'] = valor

            if bit_boleto is not None:
                payload['bitBoleto'] = bit_boleto

            if usuario_local is not None:
                payload['usuario_local'] = usuario_local

            response = self.doPOST(payload)

        return Recarga().parse_dict(self.convert_xml_to_dict(response))

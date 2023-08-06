from .exceptions import *

import json

import requests
import xmltodict


class RVapi:
    URL_PRODUCAO = "https://xml.cellcard.com.br:4443/integracao_xml.php"
    URL_HOMOLOGACAO = "https://teste.cellcard.com.br/integracao_xml.php"
    SERVER_URL = None
    IN_PRODUCTION = None
    VERSAO = 3.94
    CREDENCIAIS = {
        "loja_primaria": "teste",
        "nome_primario": "teste",
        "senha_primaria": "teste"
    }

    def __init__(self, homologacao=False):
        if homologacao is False:
            self.SERVER_URL = self.URL_PRODUCAO
            self.IN_PRODUCTION = True
        else:
            self.SERVER_URL = self.URL_HOMOLOGACAO
            self.IN_PRODUCTION = False

    def convert_xml_to_dict(self, xml):
        converted = json.loads(json.dumps(xmltodict.parse(xml.split("?>")[1], process_namespaces=True)))

        try:
            self.check_for_error(converted)
        except:
            raise

        return converted

    def set_credenciais(self, loja: str, nome: str, senha: str):
        self.CREDENCIAIS = {
            "loja_primaria": loja,
            "nome_primario": nome,
            "senha_primaria": senha
        }
        return self

    def doPOST(self, postData):
        # todo: add try except
        response = requests.request(
            "POST",
            self.SERVER_URL,
            data=postData
        )
        return response.text

    def check_for_error(self, data):
        errors = {
            '1': FoneIncompletoInvalido,
            '2': LimiteCreditoInsuficiente,
            '3': EstoqueInsuficiente,
            '4': TelefoneNaoAutorizado,
            '5': SenhaInvalida,
            '6': MaximoNumeroConexoesAtingida,
            '7': SistemaEmManutencao,
            '8': OperadoraProdutoNaoEncontrado,
            '9': CodigoInvalido,
            '10': ValorInvalido,
            '11': Timeout,
            '13': CompraExpirada,
            '14': CompraInexistente,
            '15': UsuarioLojaNaoEncontrado,
            '16': ParametrosInsuficientes,
            '17': CompraJaConfirmada,
            '18': BoletoNaoEncontrado,
            '19': ParametrosNaoEnviadosViaPOST,
            '20': CodigoTransacaoNaoInformado,
            '21': VersaoNaoInformada,
            '22': UsuarioSemNivelDeAcesso,
            '23': CobrancaAindaNaoVisualizada,
            '24': TransacaoNaoPermitida,
        }

        data = data.get('cellcard')
        print("###############################")
        print(data)
        print("###############################")
        if data.get('erro', None) is not None:
            raise errors[data['erro']['codigo']]

from .rv_api import RVapi
from .objetos import Operadora


class Transacao1(RVapi):

    OPERADORAS = None

    def execute(self, mock=None):
        if mock is not None:
            response = mock
        else:
            response = self.doPOST({
                "codigo_transacao": 1,
                "loja_primaria": self.CREDENCIAIS['loja_primaria'],
                "nome_primario": self.CREDENCIAIS['nome_primario'],
                "senha_primaria": self.CREDENCIAIS['senha_primaria'],
                "versao": self.VERSAO
            })

        response = self.convert_xml_to_dict(response)

        __cellcard_root = response.get('cellcard', None)
        __operadoras_root = __cellcard_root.get('operadoras', None)
        if __operadoras_root is not None:
            __operadoras = __operadoras_root.get('operadora', None)
            if __operadoras is not None:
                for operadora in __operadoras:
                    self.OPERADORAS = []
                    self.OPERADORAS.append(Operadora().build_from_dict(operadora))

        return response

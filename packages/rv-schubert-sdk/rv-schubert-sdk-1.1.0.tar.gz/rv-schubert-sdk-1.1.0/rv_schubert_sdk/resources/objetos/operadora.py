import pendulum

from .produto import Produto


class Operadora:
    CODIGO_OPERADORA = None
    NOME_OPERADORA = None
    ULTIMA_ATUALIZACAO_OPERADORA = None
    ESTADOS_ATUANTES = None
    PRODUTOS = None

    def build_from_dict(self, dict):
        self.CODIGO_OPERADORA = None if dict.get('codigoOperadora', None) is None else dict.get('codigoOperadora', None)
        self.NOME_OPERADORA = None if dict.get('nomeOperadora', None) is None else dict.get('nomeOperadora', None)
        self.ULTIMA_ATUALIZACAO_OPERADORA = None if dict.get('ultimaAtualizacaoOperadora', None) is None else pendulum.parse(dict.get('ultimaAtualizacaoOperadora', None))
        self.ESTADOS_ATUANTES = None if dict.get('estadosAtuantes', None) is None else dict.get('estadosAtuantes').get('estadoOperadora', None)

        __produtos = None if dict.get('produtos', None) is None else dict.get('produtos', None).get('produto', None)

        if __produtos is not None:
            self.PRODUTOS = []
            if isinstance(__produtos, list):
                for produto in __produtos:
                    self.PRODUTOS.append(Produto().build_from_dict(produto))
            else:
                self.PRODUTOS.append(Produto().build_from_dict(__produtos))

        return self

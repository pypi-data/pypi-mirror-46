from decimal import Decimal

import pendulum


class Produto:
    CODIGO_PRODUTO = None
    NOME_PRODUTO = None
    PRECO_COMPRA_PRODUTO = None
    PRECO_VENDA_PRODUTO = None
    VALIDADE_PRODUTO = None
    MODELO_RECARGA = None
    VALOR_MINIMO_PRODUTO = None
    VALOR_MAXIMO_PRODUTO = None
    VALOR_INCREMENTO_PRODUTO = None
    ULTIMA_ATUALIZACAO_PRODUTO = None
    PRECO_VARIAVEL_PRODUTO = None
    ESTADOS_PRODUTO_PIN = None

    def build_from_dict(self, dict):
        self.CODIGO_PRODUTO = None if dict.get('codigoProduto', None) is None else dict.get('codigoProduto', None)
        self.NOME_PRODUTO = None if dict.get('nomeProduto', None) is None else dict.get('nomeProduto', None)
        self.PRECO_COMPRA_PRODUTO = None if dict.get('precocompraProduto', None) is None else Decimal(dict.get('precocompraProduto'))
        self.PRECO_VENDA_PRODUTO = None if dict.get('precovendaProduto', None) is None else Decimal(dict.get('precovendaProduto'))
        self.VALIDADE_PRODUTO = None if dict.get('validadeProduto', None) is None else dict.get('validadeProduto', None)
        self.MODELO_RECARGA = None if dict.get('modeloRecarga', None) is None else dict.get('modeloRecarga', None)
        self.VALOR_MINIMO_PRODUTO = None if dict.get('valorMinimoProduto', None) is None else Decimal(dict.get('valorMinimoProduto'))
        self.VALOR_MAXIMO_PRODUTO = None if dict.get('valorMaximoProduto', None) is None else Decimal(dict.get('valorMaximoProduto'))
        self.VALOR_INCREMENTO_PRODUTO = None if dict.get('valorIncrementoProduto', None) is None else Decimal(dict.get('valorIncrementoProduto'))
        self.ULTIMA_ATUALIZACAO_PRODUTO = None if dict.get('ultima_atualizacaoProduto', None) is None else pendulum.parse(dict.get('ultima_atualizacaoProduto'))
        self.PRECO_VARIAVEL_PRODUTO = None if dict.get('precoVariavelProduto', None) is None else Decimal(dict.get('precoVariavelProduto'))
        self.ESTADOS_PRODUTO_PIN = None if dict.get('estadosProdutoPin', None) is None else dict.get('estadosProdutoPin').get('estadoProduto', None)

        return self

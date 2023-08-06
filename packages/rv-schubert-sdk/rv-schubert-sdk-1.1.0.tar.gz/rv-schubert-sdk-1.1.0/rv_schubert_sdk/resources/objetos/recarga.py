from decimal import Decimal

import pendulum


class Recarga:
    VERSAO = None
    COD_TRANSACAO = None
    REENVIO = None
    CODIGO = None
    COD_ONLINE = None
    PRODUTO = None
    PRECO = None
    FACE = None
    VENCIMENTO = None
    PAGO = None
    PIN = None
    LOTE = None
    SERIE = None
    MENSAGEM = None
    DATA_RV = None
    DDD = None
    FONE = None
    CODIGO_ASSINANTE = None
    NSU = None
    POSSUI_BOLETO = None
    RAW_DATA = None

    def parse_dict(self, data):
        data = data['cellcard']
        self.RAW_DATA = data
        self.VERSAO = None if data.get('versao', None) is None else float(data.get('versao'))
        self.COD_TRANSACAO = None if data.get('codigoTransacao', None) is None else int(data.get('codigoTransacao'))
        self.REENVIO = None if data.get('reenvio', None) is None else int(data.get('reenvio'))
        self.CODIGO = None if data.get('codigo', None) is None else int(data.get('codigo'))
        self.COD_ONLINE = data.get('cod_online', None)
        self.PRODUTO = data.get('produto', None)
        self.PRECO = None if data.get('preco', None) is None else Decimal(data.get('preco'))
        self.FACE = None if data.get('face', None) is None else Decimal(data.get('face'))
        self.VENCIMENTO = None if data.get('vencimento', None) is None else pendulum.parse(data.get('vencimento'), exact=True)
        self.PAGO = None if data.get('pago', None) is None else int(data.get('pago'))
        self.PIN = data.get('pin', None)
        self.LOTE = data.get('lote', None)
        self.SERIE = data.get('serie', None)
        self.MENSAGEM = data.get('mensagem', None)
        self.DATA_RV = None if data.get('dataRV', None) is None else pendulum.parse(data.get('dataRV'))
        self.DDD = data.get('ddd', None)
        self.FONE = data.get('fone', None)
        self.CODIGO_ASSINANTE = data.get('codigoAssinante', None)
        self.NSU = data.get('nsu', None)
        self.POSSUI_BOLETO = data.get('possuiBoleto', None)

        return self

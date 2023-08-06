class ErroRV(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class FoneIncompletoInvalido(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Fone Incompleto / Invalido [Codigo 1]")


class LimiteCreditoInsuficiente(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Limite de Crédito Insuficiente [Codigo 2]")


class EstoqueInsuficiente(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Estoque Insuficiente [Codigo 3]")


class TelefoneNaoAutorizado(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Telefone não autorizado [Codigo 4]")


class SenhaInvalida(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Senha Inválida [Codigo 5]")


class MaximoNumeroConexoesAtingida(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Máximo número de conexões atingida [Codigo 6]")


class SistemaEmManutencao(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Sistema em Manutenção [Codigo 7]")


class OperadoraProdutoNaoEncontrado(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Operadora / Produto não encontrado [Codigo 8]")


class CodigoInvalido(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Código inválido [Codigo 9]")


class ValorInvalido(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Valor Inválido [Codigo 10]")


class Timeout(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Timeout [Codigo 11]")


class CompraExpirada(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Compra Expirada [Codigo 13]")


class CompraInexistente(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Compra inexistente [Codigo 14]")


class UsuarioLojaNaoEncontrado(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Usuario/Loja não encontrados [Codigo 15]")


class ParametrosInsuficientes(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Parâmetros Insuficientes [Codigo 16]")


class CompraJaConfirmada(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Compra já confirmada [Codigo 17]")


class BoletoNaoEncontrado(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Boleto não Encontrado [Codigo 18]")


class ParametrosNaoEnviadosViaPOST(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Parametros não enviados via POST [Codigo 19]")


class CodigoTransacaoNaoInformado(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Codigo de Transacao não informado [Codigo 20]")


class VersaoNaoInformada(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Versão não informada [Codigo 21]")


class UsuarioSemNivelDeAcesso(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Usuário sem nível de acesso [Codigo 22]")


class CobrancaAindaNaoVisualizada(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Cobrança ainda não visualizada [Codigo 23]")


class TransacaoNaoPermitida(ErroRV):
    def __init__(self, *args):
        ErroRV.__init__(self, "Transação não permitida [Codigo 24]")

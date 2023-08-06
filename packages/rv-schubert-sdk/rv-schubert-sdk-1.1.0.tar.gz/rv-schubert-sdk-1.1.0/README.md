# rv-schubert-sdk
SDK de integração com a RV Tecnologia por meio de sua `API XML`

Biblioteca homologada na `RV Tecnologia` no dia `26 de março de 2019` e pronta para uso em produção.

### Dependências
Atualmente o SDK é dependente dos seguintes pacotes:

```
- xmltodict
- json
- requests
- pendulum
```


### Considerações
O objeto `Recarga`, retorna as datas por padrão usando a lib `pendulum` pois é mais pratico para calculos de datas se 
houver necessidade.

O objeto `Recarga` nada mais é que um helper para acessar a resposta padrão da `API` da `RV`.

### Homologação
Foi adicionado no arquivo de textos uma variavel chamada `RODAR_HOMOL` que por padrão tem o valor de `False`. Caso
deseje gerar os dados para homologacao, basta alterar o valor para `True` e rodar os `unittests` com o commando `python -m unittest`.

Será printado no console as informações necessárias para envio a `RV Tecnologia` para devida homologação e liberação. 

### Integrações e tarefas pendentes
#### Transações
- [X] 1  - Consulta de Produtos e Operadoras
- [X] 3  - Venda de PINs
- [X] 5  - Venda de RECARGA ONLINE
- [ ] 6  - Consulta de Status
- [X] 7  - Confirmação / Desfazimento de Transações
- [ ] 8  - Lista de Transações Pendentes
- [X] 9  - Consulta Limite de Crédito
- [ ] 10 - Consulta Lista de Boletos
- [ ] 11 - Consulta de Boleto
- [ ] 12 - Emissão Boleto Antecipado
- [ ] 13 - Consulta Totais por Dia
- [ ] 15 - Detalhe Venda
- [ ] 16 - Resumo Vendas
- [ ] 17 - Relatório Vendas
- [ ] 18 - Lista Vendas

#### Erros customizados implementados

Se você não desejar controlar os erros em um nível tão amplo, poderá utilizar `ErroRV` que é base para todos 
os erros abaixo, ou seja, todos os erros abaixo herdam de `ErroRV`.

Caso haja um `raise` de erro, você poderá tratar da seguinte forma:
 
```python
from rv_schubert_sdk import ErroRV

try:
    # seu codigo
except ErroRV as e:
    print(str(e))
```
 
Ou caso queira algo mais específico:

```python
from rv_schubert_sdk import FoneIncompletoInvalido

try:
    # seu codigo
except FoneIncompletoInvalido as e:
    print(str(e))
```

Os erros configuráveis são:

* `FoneIncompletoInvalido`
* `LimiteCreditoInsuficiente`
* `EstoqueInsuficiente`
* `TelefoneNaoAutorizado`
* `SenhaInvalida`
* `MaximoNumeroConexoesAtingida`
* `SistemaEmManutencao`
* `OperadoraProdutoNaoEncontrado`
* `CodigoInvalido`
* `ValorInvalido`
* `Timeout`
* `CompraExpirada`
* `CompraInexistente`
* `UsuarioLojaNaoEncontrado`
* `ParametrosInsuficientes`
* `CompraJaConfirmada`
* `BoletoNaoEncontrado`
* `ParametrosNaoEnviadosViaPOST`
* `CodigoTransacaoNaoInformado`
* `VersaoNaoInformada`
* `UsuarioSemNivelDeAcesso`
* `CobrancaAindaNaoVisualizada`
* `TransacaoNaoPermitida`
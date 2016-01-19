#Paypal Python API
É um módulo simples para criar pagamentos expressos e receber notificações*

* ainda não implementado

##Como utilizar?
Importamos os módulos necessários

```python
from paypal import Paypal, PaypalAuthorize, PaypalSandBoxConf
```

Se estivemos trabalhando com a SandBox, devemos instanciar sua configuração
```python
config = PaypalSandBoxConf()
```

Agora vamos requisitar a autorização junto ao PayPal, lembrando que é necessário um app ID e uma secret key.

```python
auth = PaypalAuthorize(config=config, client='ID', secret='KEY')
```

Depois de autorizado podemos então instanciar nossa compra.

```python
order = Paypal(config=config, auth=auth)
order.return_url = 'http://sua-url-de-retorno.com'
order.cancel_url = 'http://sua-url-de-cancelamento.com'
order.price = '100.00' # Valor do total da compra (note que não estamos adicionando itens)
payment = order.checkout()
```

Temos então uma pedido de pagamento criado, podemos acessar os campos do pagamento.
```python
print(payment.id)
print(payment.url)
print(payment.state)
```

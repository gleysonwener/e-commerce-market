from django.conf import settings
from .models import Product


class Carrinho(object):
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get(settings.CARRINHO_SESSION_ID)

        # criar carrinho, senão existir
        if not carrinho:
            carrinho = self.session[settings.CARRINHO_SESSION_ID] = {}
        self.carrinho = carrinho

    # fazer um loop no carrinho para adicionar e manipular
    def __iter__(self):
        for p in self.carrinho.keys():
            self.carrinho[str(p)]['product'] = Product.objects.get(pk=p)
        
        #calcula o valor total do carrinho
        for item in self.carrinho.values():
            item['total_price'] = int(item['product'].price * item['quantity'])
            yield item   # cria o valor da multiplicação

    # retornando a soma das quantidades dos produtos do carrinho
    def __len__(self):
        return sum(item['quantity'] for item in self.carrinho.values())
    
    # salvando os daddos do carrinho
    def save(self):
        self.session[settings.CARRINHO_SESSION_ID] = self.carrinho
        self.session.modified = True

    # quando clicar vai add
    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        # verificando se ja tem esse produto dentro do carrinho
        if product_id not in self.carrinho:
            self.carrinho[product_id] = {'quantity': int(quantity), 'id': product_id}

        # atualizando a quantidade de produtos do carrinho
        if update_quantity:
            self.carrinho[product_id]['quantity'] += int(quantity)

            # quando o item do carrinho for igual a 0, fazer a retirada do item ou produto
            if self.carrinho[product_id]['quantity'] == 0:
                self.remove(product_id)

        # chamando a função para chamar o carrinho
        self.save() 

    # limpando o carrinho
    def clear(self):
        del self.session[settings.CARRINHO_SESSION_ID]
        self.session.modifield = True

    # deletando o carrinho
    def remove(self, product_id):
        if product_id in self.carrinho:
            del self.carrinho[product_id]
        
        self.save()

    # somando o total do carrinho 
    def get_total_custo(self):
        for p in self.carrinho.keys():
            self.carrinho[str(p)]['product'] = Product.objects.get(pk=p)
        return int(sum(item['product'].price * item['quantity'] for item in self.carrinho.values() ))
        
    
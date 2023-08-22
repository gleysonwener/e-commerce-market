from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required 

from .carrinho import Carrinho

from .forms import OrderForm

#### stripe passo-2 antes tem que: pip install stripe
import json
import stripe
from django.http import JsonResponse
####
def add_to_carrinho(request, product_id):
    carrinho = Carrinho(request)
    carrinho.add(product_id)

    return redirect('carrinho_view')


def success(request):
    return render(request, 'loja/success.html')


def trocar_quantidade(request, product_id):
    action = request.GET.get('action', '')
    if action:
        quantity = 1
        if action == 'decrease':
            quantity = -1
        carrinho = Carrinho(request)
        carrinho.add(product_id, quantity, True)
        
    return redirect('carrinho_view')


def remove_from_carrinho(request, product_id):
    carrinho = Carrinho(request)
    carrinho.remove(product_id)

    return redirect('carrinho_view')


def carrinho_view(request):
    carrinho = Carrinho(request)
    context = {
        'carrinho': carrinho,
    }
    return render(request, 'loja/carrinho_view.html', context)


@login_required
def checar_comprar(request):
    carrinho = Carrinho(request)
    if carrinho.get_total_custo == 0:
        return redirect('carrinho_view')
    if request.method == 'POST':
        
        #### stripe passo-10 
        data = json.loads(request.body)
        ####

        p_name = data['p_name'],
        s_name = data['s_name'],
        address = data['address'],
        zip_numero = data['zip_numero'],
        city = data['city'],
        
        if p_name and s_name and address and zip_numero and city:
            form = OrderForm(request.POST)
        
            #if form.is_valid(): não precisa mais verificar o formulário após passar os dados para o json
            total_price = 0
            #### stipe passo-4
            items = []
            for item in carrinho:
                product = item['product']
                total_price += product.price * int(item['quantity'])
                ##### stripe passo-5 - preenche o dicionario com os dados para enviar para o pagamento
                items.append({
                    'price_data':{
                        'currency': 'BRL',
                        'product_data': {
                            'name': product.title,
                        },
                        'unit_amount': product.price * 100
                    },
                        'quantity': item['quantity']
                })
                ####
            
            #### stripe passo-6 - pegando a key da api do stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.create(
                payment_method_types = ['card'],  # método de pagamento
                line_items = items,    # referesse ao array em branco criado lá em cima
                mode = 'payment',
                success_url = 'http://127.0.0.1:8000/cart/success',
                cancel_url = 'http://127.0.0.1:8000/cart',
            )    

            payment_intent = session.payment_intent 
            #criando a sessão de pagamentos que queremos enviar
            ####

            """ order = form.save(commit=False)
            order.criado_por = request.user
            #### stripe passo-3
            order.esta_pago = True # adicionando o valor True para adicionar o pagamento
            order.payment_intent = payment_intent 
            ####
            order.valor_pago = total_price """

            #### stripe passo-11
            order = Order.objects.create(
                p_name = p_name,
                s_name = s_name,
                address = address,
                zip_numero = zip_numero,
                city = city,


                criado_por = request.user,
                esta_pago = True,
                payment_intent = payment_intent,
                valor_pago = total_price,
                
            )
            # order.save()

            for item in carrinho:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

                carrinho.clear()

                #### stripe passo-7 
                # return redirect('minhaconta')
                return JsonResponse({'session': session, 'order': payment_intent})
            ####
    else:
        form = OrderForm()
    context = {
        'carrinho': carrinho,
        'form': form,
        'pub_key': settings.STRIPE_PUB_KEY,
    }

    return render(request, 'loja/checar_comprar.html', context)



def search(request):
    query = request.GET.get('keyword', '') # pegando o valor que foi ditado dentro do input de pesquisar
    products = Product.objects.filter(status=Product.ATIVAR).filter(Q(title__icontains=query) | Q(description__icontains=query))
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'loja/search.html', context)


def category_detalhes(request, slug):
    category = get_object_or_404(Category, slug=slug)   
    products = category.products.filter(status=Product.ATIVAR)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'loja/category_detalhes.html', context)


def product_detalhes(request, category_slug, slug):
    products = get_object_or_404(Product, slug=slug, status=Product.ATIVAR)
    context = {
        'products': products,
    }
    return render(request, 'loja/product_detalhes.html', context)

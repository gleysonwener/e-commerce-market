from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Userprofile
from loja.forms import ProductForm
from loja.models import *

def vendor_details(request, pk):
    user = User.objects.get(pk=pk)
    products = user.Products.filter(status=Product.ATIVAR)
    context = {
       'user': user,
       'products': products
    }

    return render(request, 'userprofile/vendor_details.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':  
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            messages.success(request, 'Produto adicionado com sucesso.')
            return redirect('loja')
    else:
        form = ProductForm()
    return render(request, 'userprofile/product_form.html', {'title': 'Adicionar produto','form':form})


@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk) # seleciona o usuário da sessão e o produto pela pk
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto editado com sucesso.')
            return redirect('loja')
    else:
        form = ProductForm(instance=product)
   
    return render(request, 'userprofile/product_form.html', {
        'title': 'Editar produto',
        'product': product,
        'form':form
    })


@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk) # seleciona o usuário da sessão e o produto pela pk
    product.status = product.DELETADO
    product.save()
    messages.success(request, 'Produto deletado com sucesso.')
    return redirect('loja')


@login_required
def minha_loja(request):
    products = request.user.products.exclude(status=Product.DELETADO) # exclui o produto do usuario atual com o status deletado
    order_items = OrderItem.objects.filter(product__user=request.user)
    context = {
        'products': products,
        'order_items': order_items,
    }
    return render(request, 'userprofile/minhaloja.html', context)


@login_required
def minha_loja_pedido_detalhe(request, pk):
    order = get_object_or_404(Order, pk=pk) 
    context = {
        'order': order,
    }
    return render(request, 'userprofile/minha_loja_pedido_detalhe.html', context)


@login_required
def minha_conta(request):
    return render(request, 'userprofile/minhaconta.html')

def cadastrar(request):
   if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
           user = form.save()

           login(request,user)
           userprofile = Userprofile.objects.create(user=user)

           return redirect('frontpage')
   else:
       form = UserCreationForm()
       context = {
          'form': form,
       }

   return render(request, 'userprofile/cadastrar.html', context)
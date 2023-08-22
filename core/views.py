from django.shortcuts import render
from loja.models import Product


def frontpage(request):
    products = Product.objects.filter(status=Product.ATIVAR)[0:8]
    context = {
        'products': products,
    }
    return render(request, 'core/frontpage.html', context)



def sobre(request):
    return render(request, 'core/sobre.html')

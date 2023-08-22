from django.urls import path
from . import views


urlpatterns = [
    path('search/', views.search, name='search'),
    path('add_to_carrinho/<int:product_id>/', views.add_to_carrinho, name='add_to_carrinho'),
    path('remove-from-carrinho/<str:product_id>/', views.remove_from_carrinho, name='remove_from_carrinho'),
    
    path('trocar-quantidade/<str:product_id>/', views.trocar_quantidade, name='trocar_quantidade'),
    
    path('cart/', views.carrinho_view, name='carrinho_view'),
    path('cart/checar_comprar/', views.checar_comprar, name='checar_comprar'),
    path('cart/success/', views.success, name='success'),
    path('<slug:slug>/', views.category_detalhes, name='category_detalhes'),
    path('<slug:category_slug>/<slug:slug>/', views.product_detalhes, name='product_detalhes'),
    
]

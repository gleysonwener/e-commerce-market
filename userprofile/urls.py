from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('minhaconta/', views.minha_conta, name='minhaconta'),
    path('loja/', views.minha_loja, name='loja'),
    path('loja/order-pedido/<int:pk>/', views.minha_loja_pedido_detalhe, name='minha_loja_pedido_detalhe'),
    path('loja/add-product/', views.add_product, name='add_product'),
    path('loja/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('loja/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('vendors/<int:pk>/', views.vendor_details, name='vendor_details'),
]

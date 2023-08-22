from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw
import sys


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    

class Product(models.Model):
    RASCUNHO = 'rascunho'
    ESPERAR_APROVACAO = 'esperando aprovação'
    ATIVAR = 'ativado'
    DELETADO = 'deletado'

    STATUS_ESCOLHAS = (
        (RASCUNHO, 'Rascunho'),
        (ESPERAR_APROVACAO, 'Esperando aprovação'),
        (ATIVAR, 'Ativado'),
        (DELETADO, 'Deletado'),
    )

    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price_max = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/produto_images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/produto_images/thumbnail/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_ESCOLHAS, default=ATIVAR)

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title
    
    #chamando a função apra cria a thumbnail
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.fazer_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return '/static/img/sem-foto.jpg'
            
    # criando uma cópia da imagem a partir da imagem cadastrada no campo image
    def fazer_thumbnail(self, image, size=(300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality = 85)
        name = image.name.replace('uploads/produto_images/', '')
        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
       

class Order(models.Model):
    p_name = models.CharField(max_length=100)
    s_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zip_numero = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    valor_pago = models.IntegerField(blank=True, null=True)
    esta_pago = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=255, null=True)
    criado_por = models.ForeignKey(User, related_name='orders', on_delete= models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.price
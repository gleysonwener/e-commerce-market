# Generated by Django 4.2.4 on 2023-08-18 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0004_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/produto_images/'),
        ),
    ]

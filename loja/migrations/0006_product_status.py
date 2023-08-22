# Generated by Django 4.2.4 on 2023-08-19 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0005_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('rascunho', 'rascunho'), ('esperando aprovação', 'esperando aprovação'), ('ativado', 'ativado'), ('deletado', 'deletado')], default='ativado', max_length=50),
        ),
    ]
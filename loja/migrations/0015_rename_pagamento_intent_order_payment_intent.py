# Generated by Django 4.2.4 on 2023-08-21 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0014_remove_order_merc_id_order_esta_pago_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='pagamento_intent',
            new_name='payment_intent',
        ),
    ]
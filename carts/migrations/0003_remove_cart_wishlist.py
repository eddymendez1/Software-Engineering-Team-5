# Generated by Django 2.0.6 on 2018-07-18 21:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cart_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='wishlist',
        ),
    ]
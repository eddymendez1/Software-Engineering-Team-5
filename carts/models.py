# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from products.models import Product
from decimal import *
User = settings.AUTH_USER_MODEL


# Create your models here.
class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            print('Cart ID Exists: ', cart_id )
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj


    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user = user_obj)




class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products    = models.ManyToManyField(Product,blank =True)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    # wishlist    = models.TextField(default ='', max_length=1000)
    objects = CartManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    # print(action)
    if action =='post_add' or action =='post_remove'or action =='post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            print(x.quantity)
            total += float(str(float(x.price.strip('\'')) * int(x.quantity)))
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)



def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    instance.total = Decimal(instance.subtotal) * Decimal(1.08)

    
pre_save.connect(pre_save_cart_receiver, sender=Cart)



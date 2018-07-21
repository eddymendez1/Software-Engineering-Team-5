# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from products.models import Product
from wishlist.models import Wishlist
from .models import *
import json

# Create your views here.

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    list_obj, new_list = Wishlist.objects.new_or_get(request)
    # print(list_obj.products.get())
    return render(request,"carts/home.html", {"cart": cart_obj,"wishlist": list_obj })

def cart_update(request, *args, **kwargs):
    
    parameters = request.POST
    print(parameters)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    list_obj, new_list = Wishlist.objects.new_or_get(request)
    if 'update-quantity' in parameters:
        command =request.POST.get('update-quantity')
        product_id = request.POST.get('product_id')
        product_obj = Product.objects.get(id=product_id)
        quantity = product_obj.quantity
        if parameters['update-quantity'] == 'Increase':
            product_obj.quantity = quantity + 1
            product_obj.save()
            request.session['cart_items'] = request.session['cart_items'] + 1
            cart_obj.products.add(product_obj)
            
        elif parameters['update-quantity'] == 'Decrease':
            if quantity <  2:
                request.session['cart_items'] = request.session['cart_items'] - 1
                cart_obj.products.remove(product_obj)
            else:
                product_obj.quantity = product_obj.quantity - 1
                product_obj.save()
                request.session['cart_items'] = request.session['cart_items'] - 1
                cart_obj.products.add(product_obj)

# Wishlist Portion
    elif 'Wishlist' in parameters:
        command =request.POST.get('update-quantity')
        product_id = request.POST.get('product_id')
        product_obj = Product.objects.get(id=product_id)

        if parameters['Wishlist'] == 'Add':
            list_obj.products.add(product_obj)
            cart_obj.products.remove(product_obj)


        elif parameters['Wishlist'] == 'Remove':
            cart_obj.products.add(product_obj)
            list_obj.products.remove(product_obj)   
        
    else:
        product_id = request.POST.get('product_id')
        if product_id is not None:
            try:
                product_obj = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                print("Product does not exist")
                return redirect("cart:home")
            if product_obj in cart_obj.products.all():
                print(str(product_obj))
                cart_obj.products.remove(product_obj)
                product_obj.quantity = 1
                product_obj.save()
            else:
                cart_obj.products.add(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
    return redirect("cart:home")

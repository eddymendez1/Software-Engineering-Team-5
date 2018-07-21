from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed
from products.models import Product
from decimal import *
User = settings.AUTH_USER_MODEL

# Create your models here.

class ListManager(models.Manager):

    def new_or_get(self, request):
        list_id = request.session.get("list_id", None)
        qs = self.get_queryset().filter(id=list_id)
        if qs.count() == 1:
            new_list = False
            list_obj = qs.first()
            print('List ID Exists: ', list_id )
            if request.user.is_authenticated and list_obj.user is None:
                list_obj.user = request.user
                list_obj.save()
        else:
            list_obj = Wishlist.objects.new(user=request.user)
            new_list = True
            request.session['list_id'] = list_obj.id
            print(request.session.keys())
        return list_obj, new_list
    
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user = user_obj)


class Wishlist(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products    = models.ManyToManyField(Product,blank =True)
    objects = ListManager()

    def __str__(self):
        return str(self.id)


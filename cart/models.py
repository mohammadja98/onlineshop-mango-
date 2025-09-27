from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from shop.models import Product

class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart')
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'cart for {self.user}'
    
    def get_absolute_url(self):
        return reverse('cart:cart_detail')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"
    
    def get_absolute_url(self):
        return reverse('cart:cart_detail')
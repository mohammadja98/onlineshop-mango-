from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .cart import CartSession

@receiver(user_logged_in)
def merge_cart(sender, user, request, **kwargs):
    CartSession(request).merge_to_db(user)
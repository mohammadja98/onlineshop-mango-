from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart.cart import CartSession

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    session_cart = CartSession(request)
    session_cart.merge_to_db(user)

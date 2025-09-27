from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


from shop.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("paid", _("Paid")),
        ("shipped", _("Shipped")),
        ("delivered", _("Delivered")),
        ("cancelled", _("Cancelled")),
    ]

    user = models.ForeignKey(get_user_model(), related_name="orders", on_delete=models.CASCADE)

    first_name = models.CharField(_('First Name'),max_length=100, default="")
    last_name = models.CharField(_('Last Name'),max_length=100, default="")
    phone_number = models.CharField(_('Phone Number'),max_length=15, default="")
    address = models.CharField(_('Address'),max_length=500, blank=False)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} × {self.product}"

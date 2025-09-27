from django.apps import AppConfig
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import Cart, CartItem, Product


class CartSession:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request

        self.session = request.session
        
        cart = self.session.get('cart')


        if not cart:
            cart = self.session['cart']= {}
        
        self.cart = cart

    def add(self, product, quantity=1, replace_current_quantity=False ):
        """
        Add to specified product to the cart if it exists
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]= {'quantity': 0}
        if replace_current_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        messages.success(self.request, _("Product successfully added to cart"))

        self.save()

    def remove(self, product, ):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            messages.success(self.request, _("Product successfully removed from cart"))

            self.save()

    def save(self):
        """
        Mark session as modified to save changes
        """
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()

        return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
    

    def is_empty(self):
        if self.cart:
            return False
        return True

    def merge_to_db(self, user):
        """
        ادغام (merge) محتویات سبد سشنی داخل سبد دیتابیسیِ کاربر.
        - اگر کاربر سبد دیتابیسی نداشت، ساخته می‌شود.
        - اگر CartItem قبلاً بود، فقط quantity افزایش می‌یابد (داده از دست نمی‌رود).
        - در پایان، سبد سشنی پاک می‌شود تا منبع واحد داده، DB باشد.
        """

        cart, created = Cart.objects.get_or_create(user=user)
        for product_id, item in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
            cart_item.quantity += item["quantity"]
            cart_item.save()
        self.clear()


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"

    def ready(self):
        import cart.signals
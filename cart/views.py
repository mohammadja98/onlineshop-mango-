from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext as _

from cart.models import Cart, CartItem
from shop.models import Product
from .cart import  CartSession
from .forms import AddToCartProductForm


def cart_detail_view(request):
    
    cart_items = []
    total = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related("product")
        for item in items:
            cart_items.append({
                "product": item.product,
                "quantity": item.quantity,
                "total_price": item.product.price * item.quantity
            })
        total = sum(i["total_price"] for i in cart_items)
    else:
        cart = CartSession(request)
        for item in cart:
            cart_items.append({
                "product": item["product_obj"],
                "quantity": item["quantity"],
                "total_price": item["total_price"]
            })
        total = sum(i["total_price"] for i in cart_items)

    return render(request, "cart/cart_detail.html", {
        "cart_items": cart_items,
        "total": total,
    })


@require_POST
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        replace_current_quantity = form.cleaned_data['inplace']

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if replace_current_quantity:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, _("Product added to your account cart"))
        else:
            cart = CartSession(request)
            cart.add(product, quantity, replace_current_quantity=replace_current_quantity)

    return redirect("cart:cart_detail")


def remove_from_cart_view(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(cart=request.user.cart, product=product)
            cart_item.delete()
            messages.success(request, _("Product removed from your cart"))
        except CartItem.DoesNotExist:
            messages.warning(request, _("This product is not in your cart"))
    else:
        cart = CartSession(request)
        cart.remove(product)

    return redirect("cart:cart_detail")


@require_POST
def clear_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if cart.items.exists():
            cart.items.all().delete()
            messages.success(request, _('All products successfully removed from your account cart'))
        else:
            messages.warning(request, _('Your account cart is already empty'))
    else:
        cart = CartSession(request)
        if len(cart):
            cart.clear()
            messages.success(request, _('All products successfully removed from your session cart'))
        else:
            messages.warning(request, _('Your session cart is already empty'))

    return redirect("cart:cart_detail")


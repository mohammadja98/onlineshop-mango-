
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .models import OrderItem
from .forms import OrderForm
from cart.cart import CartSession  
from cart.models import Cart

@login_required
def order_create_view(request):
    order_form = OrderForm()
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.select_related("product")
            if not cart_items.exists():
                messages.warning(request, _("your cart is empty"))
                return redirect('cart:cart_detail')
        except Cart.DoesNotExist:
            messages.warning(request, _("cart not found"))
            return redirect('cart:cart_detail')
    else:
        cart = CartSession(request)
        if len(cart) == 0:
            messages.warning(request, _("your cart is empty"))
            return redirect('cart:cart_detail')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            # Create order items based on authentication status
            if request.user.is_authenticated:
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order_obj,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )
                # Clear the database cart
                cart.items.all().delete()
            else:
                for item in cart:
                    product = item['product_obj']
                    OrderItem.objects.create(
                        order=order_obj,
                        product=product,
                        quantity=item['quantity'],
                        price=product.price,
                    )
                # Clear the session cart
                cart.clear()

            # Update user profile
            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()
            messages.success(request, _("order sucsessful registered ✅"))
            return redirect('cart:cart_detail')
        else:
            messages.error(request, _("The order form is invalid. Please try again."))

    return render(request, 'orders/order_create.html', {
        'form': order_form,
    })

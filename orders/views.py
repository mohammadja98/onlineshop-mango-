
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import CartSession  # your session-based cart class

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart,CartItem
from .forms import OrderForm
from cart.cart import CartSession

@login_required
def order_create_view(request):
    order_form = OrderForm()
    
    # Initialize cart based on authentication status
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.select_related("product")
            if not cart_items.exists():
                return redirect('cart:cart_detail')
        except Cart.DoesNotExist:
            return redirect('cart:cart_detail')
    else:
        cart = CartSession(request)
        if len(cart) == 0:
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

            return redirect('cart:cart_detail')  # Or redirect to an order confirmation page

    return render(request, 'orders/order_create.html', {
        'form': order_form,
    })

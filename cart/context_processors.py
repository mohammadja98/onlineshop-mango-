from .models import Cart
from .cart import CartSession

def cart(request):
    return {'cart': CartSession(request)}


def cart_context(request):
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

    return {
        "cart_items": cart_items,
        "cart_total": total,
        "cart_count": len(cart_items),
    }

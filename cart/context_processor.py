from .models import CartItem, Cart
from .views import _cart_id

def cart_count(request):

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).count()
        return {'cart_count':cart_items}
        
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True).count()
        return {'cart_count':cart_items}
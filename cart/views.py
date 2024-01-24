from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from .models import Cart, CartItem, Coupon
from django.utils import timezone
# Create your views here.

def _cart_id(request):

    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def Add_To_Cart(request, product_id):
    current_user = request.user
    product =  get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))

        if current_user.is_authenticated:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except:
                cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()       

            cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()

            if cart_item_exist:
                cart_item = CartItem.objects.get(product=product, user=current_user)
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    user=current_user,
                    product=product, 
                    cart=cart,
                    quantity=quantity,
                    )

                cart_item.save()

        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except:
                cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()       

            cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()

            if cart_item_exist:
                cart_item = CartItem.objects.get(product=product, cart=cart)
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product=product, 
                    cart=cart,
                    quantity=quantity,
                    )

                cart_item.save()

    return redirect('cart:view_cart')


def View_Cart(request):
    current_user = request.user
    cart_items = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    cart_total = 0
    sub_total = 0
    shipping_cost = 10

    for item in cart_items:
        sub_total += float(item.product.price * item.quantity)
    cart_total += shipping_cost + sub_total

    if cart.coupon and cart.coupon.active:
        discount_amount = ((cart_total / 100.00 ) * float(cart.coupon.discount))
        cart_total =cart_total - discount_amount
    else:
        discount_amount = 0
    context = {'cart_items':cart_items, 'cart_total':cart_total, 'sub_total':sub_total, 'cart_coupon': cart.coupon}

    return render(request, 'cart/shopping-cart.html', context)


def Clear_Cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart.delete()
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart.delete()
        except:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.delete()

    return redirect('cart:view_cart')


def Update_Cart(request):
    current_time = timezone.now().date()

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        coupon = Coupon.objects.get(code=coupon_code)

        if coupon.expiry_date > current_time and coupon.active:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart.coupon = coupon
                cart.save()
            except:
                cart = Cart.objects.create(cart_id=_cart_id(request))
                cart.coupon = coupon
                cart.save()

        if coupon.active_date > current_time:
            return redirect('cart:view_cart')


    else:
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                cart_item_id = key.replace('quantity_', '')
                try:
                    cart_item = CartItem.objects.get(id=cart_item_id)
                    if cart_item.product.is_stock:
                        cart_item.quantity = int(value)
                        cart_item.save()
                except CartItem.DoesNotExist:
                    return redirect('cart:view_cart')
    
    return redirect('cart:view_cart')

def Cart_Item_Remove(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart:view_cart')


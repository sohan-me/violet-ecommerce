from django.shortcuts import render, redirect, HttpResponse
from store.models import Product
from cart.models import CartItem
from django.db.models import Sum, F
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_order_number


# Create your views here.

from django.shortcuts import render, redirect
from django.db.models import F, Sum
from .models import Order, OrderProduct, Payment
from accounts.models import Account

def CheckOut(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user_cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    total = user_cart_items.annotate(item_total=F('quantity') * F('product__price')).aggregate(total_cost=Sum('item_total'))['total_cost'] or 0
    total_product = user_cart_items.aggregate(total_product=Sum(F('quantity')))['total_product'] or 0
    tax = 20
    grand_total = total + tax

    if request.method == 'POST':
        # Collect user data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        order_number = generate_order_number()

        # Create the order
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            order_total=grand_total,
            status='Pending',
            first_name=first_name,
            last_name=last_name,
            street_address=street_address,
            city=city,
            country=country,
            post_code=postcode,
            phone=phone,
            payment_method=payment_method,
        )

        # Create order items
        for item in user_cart_items:
            OrderProduct.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True,
            )

        # Clear the cart
        user_cart_items.delete()

        # Send order receive mail to user
        mail_subject = 'Cat Shop: We received your order.'
        mail_messages = f'''Dear {first_name} {last_name},\n\nThank you for placing your order with Cat Shop!\n\nYour order number is: {order_number}\n\nWe're currently holding your order, pending payment confirmation. Once we receive your payment, we'll begin processing your order and send you a confirmation email with shipping details.\nIf you have any questions, please don't hesitate to contact us.\n\nSincerely,\nCat Shop'''
        email_send = EmailMessage(mail_subject, mail_messages, settings.EMAIL_HOST_USER, to=[request.user.email])
        email_send.fail_silently = False
        email_send.send()

        # Redirect to payment page or success page based on payment method
        if payment_method == 'SSLCommerz':
            return redirect('orders:initiate_payment')
        else:
            return redirect('store:Home')

    context = {
        'cart_items': user_cart_items,
        'total': total,
        'total_product': total_product,
        'grand_total': grand_total,
    }
    return render(request, 'orders/checkout.html', context)




def InitiatePayment(request):
	return HttpResponse('Payment success')



def OrderByUser(request):
    orders = Order.objects.filter(user=request.user)
    unpaid_orders = orders.objects.filter(status='Pending')
    paid_orders = orders.objects.filter(status='Confirmed')
    pass
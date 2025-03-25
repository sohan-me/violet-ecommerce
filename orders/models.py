from django.db import models
from store.models import Product
from accounts.models import Account
from cart.models import Coupon


from django.utils import timezone

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    phone = models.CharField(max_length=20, blank=True, null=True)
    order_number = models.CharField(max_length=50, unique=True)
    street_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=300, null=True, blank=True)
    post_code = models.CharField(max_length=300, null=True, blank=True)
    order_total = models.FloatField()
    payment_method = models.CharField(max_length=55)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status not in ['Pending', 'Cancelled']:
            self.is_ordered = True

            order_products = self.order_product.all()
            product_updates = []
            for item in order_products:
                item.product.stock_quantity -= item.quantity
                product_updates.append(item.product)
            Product.objects.bulk_update(product_updates, ['stock_quantity'])


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


class Payment(models.Model):
    PAYMENT_METHOD = (
        ('SSLCommerz', 'SSLCommerz'),
        ('Cash On Delivery', 'Cash On Delivery'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
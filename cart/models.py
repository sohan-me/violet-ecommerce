from django.db import models
from store.models import Product
from django.contrib.auth.models import User
# Create your models here.



class Coupon(models.Model):
    code = models.CharField(max_length=150, unique=True)
    discount = models.PositiveIntegerField(help_text='Discount in percentage')
    active = models.BooleanField(default=False)
    active_date = models.DateField(help_text='Format: DD-MM-YEAR')
    expiry_date = models.DateField(help_text='Format: DD-MM-YEAR')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class Cart(models.Model):
    cart_id = models.CharField(max_length=150, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.cart_id



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title

    def item_total(self):
        return float(self.product.price * self.quantity)

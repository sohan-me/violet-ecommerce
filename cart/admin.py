from django.contrib import admin
from .models import Cart, CartItem, Coupon
# Register your models here.

class AdminCouponView(admin.ModelAdmin):
    list_display = ['id', 'code', 'discount', 'active', 'active_date', 'expiry_date']
    list_editable = ['active']

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon, AdminCouponView)
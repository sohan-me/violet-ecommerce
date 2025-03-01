from django.contrib import admin
from .models import Order, Payment, OrderProduct
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
# Register your models here.



class PaymentAdmin(admin.ModelAdmin):
	list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']
	search_fields = ['payment_id']
	list_filter = ['status']



class OrderProductInline(admin.TabularInline):
	model = OrderProduct
	readonly_fields = ['order', 'quantity', 'product_price', 'ordered']
	extra = 0


class AdminOrderView(admin.ModelAdmin):

	list_display = ['order_number', 'user', 'first_name', 'last_name', 'status', 'is_ordered', 'created_at', 'updated_at']
	list_filter = ['is_ordered']
	search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
	inlines = [OrderProductInline]
	list_per_page = 20


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, AdminOrderView)
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart:<int:product_id>/', views.Add_To_Cart, name='add_to_cart'),
    path('cart/', views.View_Cart, name='view_cart'),
    path('clear-cart/', views.Clear_Cart, name='clear_cart'),
    path('update-cart/', views.Update_Cart, name='update_cart'),
    path('cart-item-remove/<int:cart_item_id>/', views.Cart_Item_Remove, name='cart_item_remove'),

]
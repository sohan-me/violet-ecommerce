from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('check-out/', views.CheckOut, name='CheckOut'),
    path('initiate_payment/', views.InitiatePayment, name='initiate_payment'),
    path('total_orders/', views.OrderByUser, name='orders_by_user'),
   

]
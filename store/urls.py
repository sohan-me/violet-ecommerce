from django.urls import path
from . import views

app_name = 'store'


urlpatterns = [
    path('', views.Home, name='Home'),
    path('product/<slug:slug>/', views.Product_Details, name='Product_Details'),
    path('shop/', views.Shop, name='Shop'),
    path('category/<slug:slug>/', views.Category_Details, name='Category_Details'),
    path('search-result/', views.Search, name='search-products'),
    path('contact/', views.ContactUs, name='Contact'),
    path('about/', views.AboutUs, name='about'),


]
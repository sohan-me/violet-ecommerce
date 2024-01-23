from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import *
# Create your views here.

def Home(request):
    featured_categories = Category.objects.filter(featured=True)
    categories = Category.objects.all()
    featured_products = Product.objects.filter(featured=True)
    slider = Slider.objects.filter(show=True)
    
    paginator = Paginator(featured_products, 4)
    page = request.GET.get('page')

    try:
        featured_products = paginator.page(page)
    except PageNotAnInteger:
        featured_products = paginator.page(1)
    except EmptyPage:
        featured_products = paginator.page(paginator.num_pages)



    context = {
        'featured_categories':featured_categories,
        'featured_products':featured_products,
        'slider':slider,
        'categories':categories,
    }
    return render(request, 'main/Home.html', context)



def Product_Details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    relatable_product = Product.objects.filter(category=product.category).exclude(pk=product.pk)
    context = {
        'product':product,
        'relatable_product':relatable_product[:4]
    }
    return render(request, 'product/product-page.html', context)


def Category_Details(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    p_count = products.count()

    paginator = Paginator(products, 4)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    context = {
        'category':category,
        'products':products,
        'p_count':p_count,
    }
    return render(request, 'product/categories.html', context)



def Search(request):

    key = request.GET.get('key')
    products = Product.objects.filter(
        Q(title__icontains=key) |
        Q(description__icontains=key)
    )
    p_count = products.count()

    paginator = Paginator(products, 8)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
            
    context = {
        'products':products,
        'key':key,
        'p_count':p_count,
    }
    return render(request, 'main/search-result.html', context)

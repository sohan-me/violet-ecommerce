from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Prefetch

from .models import *
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

def Home(request):
    featured_categories = Category.objects.filter(featured=True)
    in_stock_products = Product.objects.filter(is_stock=True)
    categories = Category.objects.filter(featured=True).prefetch_related(Prefetch('products', queryset=in_stock_products))
    featured_products = Product.objects.filter(featured=True)
    slider = Slider.objects.filter(show=True)
    lookbook = Lookbook.objects.filter(show=True).first()


    context = {
        'featured_categories':featured_categories,
        'featured_products':featured_products,
        'slider':slider,
        'categories':categories,
        'lookbook':lookbook,
    }
    return render(request, 'main/Home.html', context)


def Shop(request):
    products = Product.objects.filter(is_stock=True)
    p_count = products.count()
    paginator = Paginator(products, 8)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    context = {'products':products, 'p_count':p_count}
    return render(request, 'product/shop.html', context)


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
        Q(description__icontains=key),
        is_stock=True
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



def ContactUs(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            contact_object = Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                subject=subject,
                message=message
                )
            contact_object.save()

            mail_subject = 'Cat Shop: We received your message.'
            mail_messages = f'''Dear {first_name} {last_name},\nThis email confirms that we have received your inquiry.\nWe are currently reviewing your request and will contact you shortly with an update on its status.\nThank you for your patience.\nSincerely,\nCat Shop'''
            email_send = EmailMessage(mail_subject, mail_messages, settings.EMAIL_HOST_USER, to=[email])
            email_send.fail_silently = False
            email_send.send()

            return redirect('store:Home')

    context = {'form':form}
    return render(request, 'main/contact.html', context)



def AboutUs(request):
    return render(request, 'main/about.html')
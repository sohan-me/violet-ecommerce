from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class StoreDetails(models.Model):
    trade_license = models.CharField(max_length=200, null=True, blank=True)
    brand_bin = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = 'Store Detail'
        verbose_name_plural='Store Details'

    def __str__(self):
        return self.trade_license if self.trade_license else 'Store Details' 


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, max_length=200)
    featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title
    




class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True, max_length=250)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product/food/', blank=True, null=True)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True, default='N/A')
    stock_quantity = models.PositiveIntegerField()
    is_stock = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
    
    def save(self, *args, **kwargs):
        if self.stock_quantity == 0:
            self.is_stock = False
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Slider(models.Model):
    title = models.CharField(max_length=50)
    banner = models.ImageField(upload_to='banners/')
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def initial_part(self):
        year = self.title.split(' ')[0]
        return year
    def final_part(self):
        rest = self.title.split(' ')[1]
        return rest


class Lookbook(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='banners/')
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Contact(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    mark_as_read = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    


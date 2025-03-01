from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

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
    is_stock = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

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



class Contact(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    mark_as_read = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    


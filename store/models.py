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
    price = models.FloatField()
    thumbnail = models.URLField()
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

    


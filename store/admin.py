from django.contrib import admin
from .models import Category, Product, Slider

# Register your models here.

class AdminCategoryView(admin.ModelAdmin):
    list_display = ['id', 'title', 'featured', 'created_date']
    prepopulated_fields = {'slug': ('title', )}

class AdminProductView(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'featured', 'price', 'updated_date', 'created_date']
    list_filter = ['category', 'price']
    list_editable = ['featured']
    prepopulated_fields = {'slug': ('title', )}

class AdminSliderView(admin.ModelAdmin):
    list_display = ['id', 'title', 'show']


admin.site.register(Category, AdminCategoryView)
admin.site.register(Product, AdminProductView)
admin.site.register(Slider, AdminSliderView)

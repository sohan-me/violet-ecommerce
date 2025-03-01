from django.contrib import admin
from .models import Category, Product, Slider, Contact

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



class AdminContactView(admin.ModelAdmin):
    list_display = ['email', 'subject', 'first_name', 'last_name', 'mark_as_read']
    search_fields = ['email']
    list_filter = ['mark_as_read']
    list_editable = ['mark_as_read']

admin.site.register(Category, AdminCategoryView)
admin.site.register(Product, AdminProductView)
admin.site.register(Slider, AdminSliderView)
admin.site.register(Contact, AdminContactView)



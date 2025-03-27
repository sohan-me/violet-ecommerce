from .models import Category, StoreDetails

def categories(request):
    categories = Category.objects.all()
    store_details = StoreDetails.objects.all().first()
    return {'categories': categories, 'store_details':store_details}
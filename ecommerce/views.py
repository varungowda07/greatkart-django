from django.shortcuts import render
from store.models import Product

def home(request):
    products=Product.objects.all()
    # for product in products:
    #     print(products.product_name)
    
    context={'products':products}
    return render(request,'home.html',context)
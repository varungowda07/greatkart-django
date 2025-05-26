from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from carts.models import CartItem
from carts.views import get_session_id
from . models import Product
from category.models import Category
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.db.models import Q

def store(request,category_slug=None):
    if category_slug != None:
        category=get_object_or_404(Category,slug=category_slug) 
        products=Product.objects.filter(category=category,is_available=True)
        product_count=products.count()
        paginator = Paginator(products, 6)  # Show 6 products per page
        page = request.GET.get('page')  # Get current page number from request
        paged_products = paginator.get_page(page)
    else:
        products=Product.objects.filter(is_available=True)
        product_count=products.count()
        paginator = Paginator(products, 6)  # Show 6 products per page
        page = request.GET.get('page')  # Get current page number from request
        paged_products = paginator.get_page(page)
    context={'products':paged_products,'product_count':product_count}
    return render(request,'store/store.html',context)


def product_detail(request, category_slug, product_slug):
    
    single_product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    cart_item=CartItem.objects.filter(cart__cart_id=get_session_id(request),product=single_product).exists()
    
    context = {'single_product': single_product,
               'cart_item':cart_item}
    return render(request, 'store/product_detail.html', context)
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            
            products=Product.objects.filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count=products.count()
    context={'products':products,'product_count':product_count}
    return render(request,'store/store.html',context)

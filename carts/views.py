from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart,CartItem


def get_session_id(request):
    cart =request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)

    try:
        cart=Cart.objects.get(cart_id=get_session_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=get_session_id(request))
    cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
        
    cart_item.save()
    return redirect('cart')

def decrement_cart(request,product_id):
    cart=Cart.objects.get(cart_id=get_session_id(request))
    product=Product.objects.get(id=product_id)

    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity-=1
        cart_item.save()
        return redirect('cart')
    else:
        cart_item.delete()
        return redirect('cart')
    
def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=get_session_id(request))
    product=Product.objects.get(id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,cart_items=None,quantity=0):
    try:
        cart=Cart.objects.get(cart_id=get_session_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            cart_item.subtotal = cart_item.product.price * cart_item.quantity
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
    except ObjectNotExist:
        pass
    intrest=(total*10)/100
    final_total=total+intrest
    cart_item_count=cart_items.count()
    context={
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'intrest':intrest,
        'final_total':final_total,
        'cart_item_count':cart_item_count,
    }

    return render(request,'carts/cart.html',context)

from django.shortcuts import render,redirect
from store.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



def get_session_id(request):
    cart =request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

# def add_cart(request,product_id):
#     product=Product.objects.get(id=product_id)

#     try:
#         cart=Cart.objects.get(cart_id=get_session_id(request))
#     except Cart.DoesNotExist:
#         cart=Cart.objects.create(cart_id=get_session_id(request))
#     cart.save()
#     try:
#         cart_item=CartItem.objects.get(product=product,cart=cart)
#         cart_item.quantity+=1
#     except CartItem.DoesNotExist:
#         cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
        
#     cart_item.save()
#     return redirect('cart')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = get_session_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    if request.user.is_authenticated:
        try:
            # Try to get item with this product for the logged-in user
            cart_item = CartItem.objects.get(product=product, cart=cart, user=request.user)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            # Try to merge guest item if it exists (user=None)
            try:
                guest_item = CartItem.objects.get(product=product, cart=cart, user=None)
                guest_item.user = request.user
                guest_item.quantity += 1
                guest_item.save()
            except CartItem.DoesNotExist:
                # Create a new one if no existing item found
                CartItem.objects.create(product=product, cart=cart, user=request.user, quantity=1)
    else:
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart, user=None)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(product=product, cart=cart, user=None, quantity=1)

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
    # cart=Cart.objects.get(cart_id=get_session_id(request))
    # product=Product.objects.get(id=product_id)
    # cart_item=CartItem.objects.get(product=product,cart=cart)
    # cart_item.delete()
    # return redirect('cart')
    try:
        if request.user.is_authenticated:
            # Logged-in user: remove by user
            CartItem.objects.filter(product_id=product_id, user=request.user).delete()
        else:
            # Guest user: remove by session cart
            cart = Cart.objects.get(cart_id=get_session_id(request))
            CartItem.objects.filter(product_id=product_id, cart=cart, user=None).delete()
    except Cart.DoesNotExist:
        # Cart doesn't exist: nothing to remove
        pass

    return redirect('cart')
def cart(request,total=0,cart_items=None,quantity=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart, user=None, is_active=True)
    except (Cart.DoesNotExist, ObjectDoesNotExist):
        cart_items = []

    # Calculate total, quantity, and subtotal for each cart item
    for cart_item in cart_items:
        cart_item.subtotal = cart_item.product.price * cart_item.quantity
        total += cart_item.subtotal
        quantity += cart_item.quantity

    interest = (total * 10) / 100
    final_total = total + interest
    cart_item_count = len(cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'intrest': interest,
        'final_total': final_total,
        'cart_item_count': cart_item_count,
    }

    return render(request, 'carts/cart.html', context)

@login_required(login_url='login')
def checkout(request,total=0,cart_items=None,quantity=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_session_id(request))
            cart_items = CartItem.objects.filter(cart=cart, user=None, is_active=True)
    except(Cart.DoesNotExist, ObjectDoesNotExist):
        cart_items = []

    # Calculate total, quantity, and subtotal for each cart item
    for cart_item in cart_items:
        cart_item.subtotal = cart_item.product.price * cart_item.quantity
        total += cart_item.subtotal
        quantity += cart_item.quantity

    interest = (total * 10) / 100
    final_total = total + interest
    cart_item_count = len(cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'intrest': interest,
        'final_total': final_total,
        'cart_item_count': cart_item_count,
    }


    return render(request, 'carts/checkout.html', context)


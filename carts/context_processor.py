from .models import CartItem, Cart
from .views import get_session_id

def cart_item_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            count = CartItem.objects.filter(user=request.user, is_active=True).count()
        else:
            cart = Cart.objects.get(cart_id=get_session_id(request))
            count = CartItem.objects.filter(cart=cart, user=None, is_active=True).count()
    except:
        pass
    return {'cart_item_count': count}

from django.urls import path
from . import views

urlpatterns=[
    path('',views.cart,name='cart'),
    path('add-cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('decrement-cart/<int:product_id>',views.decrement_cart,name='decrement_cart'),
    path('remove-cart/<int:product_id>',views.remove_cart,name='remove_cart')
]

from django.urls import path
from . import views

urlpatterns = [
    path('search/',views.search,name='search'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('<slug:category_slug>/',views.store,name='category_slug'),
    path('',views.store,name='store'),
    
]

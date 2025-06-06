from django.db import models
from django.contrib.auth.models import User


from store.models import Product

class Cart(models.Model):
    cart_id=models.CharField(max_length=350, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(blank=True)
    is_active=models.BooleanField(blank=True,default=True)

    def __unicode__(self):
        return self.product
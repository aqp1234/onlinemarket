from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + "'s cart"

    def get_cart_total(self):
        total = 0
        for item in self.cartitems.all():
            total += item.get_product_total()
        return total
    
    def get_quantity(self):
        quantity = 0
        for item in self.cartitems.all():
            quantity += item.quantity
        return quantity

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField()

    def get_product_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

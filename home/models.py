from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class productCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    imageTag = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class productSubcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(productCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class productItem(models.Model):
    subcategory = models.ForeignKey(productSubcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100)
    price = models.FloatField()
    onDeal = models.BooleanField(null=True, blank=True)
    imageTag = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(productItem, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(productItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
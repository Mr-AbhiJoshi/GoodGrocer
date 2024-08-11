from django.contrib import admin
from .models import productCategory, productSubcategory, productItem, Cart, CartItem, Contact


# Register your models here.
admin.site.register(productCategory)
admin.site.register(productSubcategory)
admin.site.register(productItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Contact)
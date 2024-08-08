from django.contrib import admin
from .models import productCategory, productSubcategory, productItem


# Register your models here.
admin.site.register(productCategory)
admin.site.register(productSubcategory)
admin.site.register(productItem)
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
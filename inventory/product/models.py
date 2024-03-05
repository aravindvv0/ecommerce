from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    categoryname=models.CharField(max_length=40)
    def __str__(self):
        return self.categoryname
    
class Brand(models.Model):
    brandname=models.CharField(max_length=15)
    def __str__(self):
         return self.brandname
    
class Product(models.Model):
    productname=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    description=models.TextField(null=True)
    catid = models.ForeignKey(Category, on_delete=models.CASCADE)
    brandid = models.ForeignKey(Brand, on_delete=models.CASCADE)
    def __str__(self):
        return self.productname
    
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.product.productname} - {self.user.username}'
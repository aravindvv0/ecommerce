from rest_framework import serializers
import django_filters
from .models import Product,Inventory
from django.contrib.auth.models import User
print("remote changes")
class ProductSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productname', 'price','catid','brandid']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerialaizer() 
    user = UserSerializer()
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name='product__productname', lookup_expr='icontains')

    class Meta:
        model = Inventory
        fields = ['product'] 

class InventorySerializerWithProduct(serializers.ModelSerializer):
    product = ProductSerialaizer() 
    user = UserSerializer()
    class Meta:
        model = Inventory
        fields = '__all__'

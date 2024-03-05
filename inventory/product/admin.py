from django.contrib import admin
from .models import Product,Category,Brand,Inventory
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ["productname","product_image","price","catid","brandid"]

class InventoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields =["id","product","quantity","user"]

class CategoryAdmin(admin.ModelAdmin):
    fields = ["categoryname"]

class BrandAdmin(admin.ModelAdmin):
    fields = ["brandname"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Inventory, InventoryAdmin)

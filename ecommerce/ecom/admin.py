from django.contrib import admin
from .models import *
from  django.contrib.auth.models import Group
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import reverse


# Register your models here.
# class Myadmin(admin.AdminSite):
#     def myviews(self,request):

#         return format_html('<a class="button" href="{}">Button</a>')

  

# class CustomerAdmin(admin.ModelAdmin):
#     list_display=('id','name','email','mobile','active','registerdate')
# admin.site.register(Customer, CustomerAdmin)

# class ProductAdmin(admin.ModelAdmin):
#     list_display=('id','name','product_image','price','description','active','scatid_id','brand_id')
# admin.site.register(Product, ProductAdmin)

# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display=('id','subcategoryname','active')
# admin.site.register(Subcategory, SubCategoryAdmin)

# class CategoryAdmin(admin.ModelAdmin):
#     list_display=('id','categoryname','active')
# admin.site.register(Category, CategoryAdmin)

# class BrandAdmin(admin.ModelAdmin):
#     list_display=('brandid','brandname','active')
# admin.site.register(Brand, BrandAdmin)

# class OrderAdmin(admin.ModelAdmin):
#      list_display=('order_id','customer','location','payment','amount','status','order_date','deliver_date')
# admin.site.register(Orders, OrderAdmin)

# class OrderdetailAdmin(admin.ModelAdmin):
#      list_display=("id","get_id",'product','quantity','unitprice','totalprice')
#      def get_id(self, obj):
#          return obj.order.order_id
#      get_id.admin_order_field = 'order'
#      get_id.short_description = 'Order id'    
# admin.site.register(Orderdetails, OrderdetailAdmin)

# class LocationAdmin(admin.ModelAdmin):
#     list_display=('id','address','district','city','pin','customer_id')
# admin.site.register(Location, LocationAdmin)

# class StockAdmin(admin.ModelAdmin):
#     list_display=('id','stockid','product','quantity','purchasedate')
# admin.site.register(Stock, StockAdmin)
# # Register your models here.

# admin.site.unregister(Group)

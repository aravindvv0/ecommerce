from venv import CORE_VENV_DEPS
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Customer(models.Model):
#     # user=models.OneToOneField(User,on_delete=models.CASCADE)
#     # profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
#     name = models.CharField(max_length=20)
#     email = models.CharField(max_length=20)
#     password = models.CharField(max_length=6)
#     mobile = models.CharField(max_length=20)
#     active = models.BooleanField(default=True)
#     role=models.IntegerField(null=True)
#     registerdate = models.DateTimeField(auto_now_add=True, blank=True)
#     # @property
#     # def get_name(self):
#     #     return self.user.first_name+" "+self.user.last_name
#     # @property
#     # def get_id(self):
#     #     return self.user.id
#     def __str__(self):
#          return self.name
# class Location(models.Model):
#     address = models.CharField(max_length=40)
#     city = models.CharField(max_length=15,null=True)
#     district = models.CharField(max_length=10,null=True)
#     pin = models.IntegerField(null=True)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     def __str__(self):
#        return self.address
     
# class Vendor(models.Model):

#     vname = models.CharField(max_length=20)
#     vemail = models.CharField(max_length=20)
#     vpassword = models.CharField(max_length=12)
#     vcontact = models.CharField(max_length=20)
#     vaddress = models.CharField(max_length=50)
#     vlocation =  models.CharField(max_length=50)
#     vactive = models.BooleanField(default=True)
#     vurl  =  models.CharField(max_length=40)
#     vlogo= models.ImageField(upload_to='logo/',null=True,blank=True)
#     registerdate = models.DateTimeField(auto_now_add=True, blank=True)

      
# class Category(models.Model):
#     categoryname=models.CharField(max_length=40)
#     categorydesc=models.CharField(max_length=40)
#     active = models.BooleanField(default=True)
#     # def __str__(self):
#     #     return self.name 
# class Subcategory(models.Model):
#     subcategoryname=models.CharField(max_length=40)
#     subcategorydesc=models.CharField(max_length=40)
#     catid = models.ForeignKey(Category, on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)
#     def __str__(self):
#         return self.subcategoryname 
# class Brand(models.Model):
#     brandid = models.IntegerField(primary_key=True)
#     brandname=models.CharField(max_length=15)
#     active = models.BooleanField(default=True)
#     def __str__(self):
#          return self.brandname

# class Product(models.Model):
#     name=models.CharField(max_length=40)
#     product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
#     price = models.PositiveIntegerField()
#     desc=models.CharField(max_length=50,null=True)
#     description=models.TextField(null=True)
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True)
#     scatid = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
#     active = models.BooleanField(default=True)
#     def __str__(self):
#         return self.name

# class Stock(models.Model):
#     stockid = models.IntegerField()
#     product = models.ForeignKey(Product, on_delete=models.CASCADE) 
#     quantity = models.IntegerField()
#     purchaseprice = models.FloatField()
#     sellingprice = models.FloatField(default=1000)
#     purchasedate = models.DateTimeField(auto_now_add=True)
#     expirydate = models.DateField(null=True)
#     active = models.BooleanField(default=True)
   

# class Cart(models.Model):
#     customer =  models.ForeignKey(Customer, on_delete=models.CASCADE)
#     productid =  models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     unitprice = models.FloatField(max_length=10)
#     totalprice = models.FloatField(max_length=10)
#     def __str__(self):
#         return self.customer

# class Orders(models.Model):
#     STATUS =(
#         ('Order Confirmed','Order Confirmed'),
#         ('Out for Delivery','Out for Delivery'),
#         ('Delivered','Delivered'),
#     )
#     order_id=models.AutoField(primary_key=True)
#     customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
#     location=models.ForeignKey('Location',on_delete=models.CASCADE,null=True)
#     payment=models.CharField(max_length=15,null=True)
#     amount=models.FloatField(max_length=10, null=True)
#     order_date= models.DateField(auto_now_add=True,null=True)
#     deliver_date= models.DateField(null=True)
#     status=models.IntegerField(null=True)
#     status2=models.CharField(max_length=50,null=True,choices=STATUS)
#     # def __str__(self):
#     #       return self.order_id
   

# class Orderdetails(models.Model):
#     order=models.ForeignKey('Orders', on_delete=models.CASCADE,null=True)
#     product=models.ForeignKey('Product', on_delete=models.CASCADE,null=True)
#     quantity = models.IntegerField()
#     unitprice = models.FloatField(max_length=10)
#     totalprice = models.FloatField(max_length=10)
#     # def __str__(self):
#     #       return self.name

# class Feedback(models.Model):
#     name=models.CharField(max_length=40,null=True)
#     feedback=models.CharField(max_length=500,null=True)
#     date= models.DateField(auto_now_add=False,null=True)
#     filepath = models.FileField(upload_to='static/', null=True,verbose_name="")
#     def __str__(self):
#         return self.name

# class Chumma(models.Model):
#     id = models.AutoField(primary_key=True,default=1000)
#     name = models.CharField(max_length=20,null=True)
#     userid = models.ForeignKey(Customer,null=True,on_delete=models.DO_NOTHING)

    

# class Payment(models.Model):
#     payid=models.IntegerField(primary_key=True)  
#     cardnumber=models.BigIntegerField()
#     cardholdername=models.CharField(max_length=20)
#     expirymonth=models.CharField(max_length=15)
#     expiryyear = models.IntegerField()
#     customer = models.ForeignKey('Customer', on_delete=models.CASCADE) 
#     cvv = models.SmallIntegerField()




# class Reorder(models.Model):
#     reorder_id=models.AutoField(primary_key=True)
#     vendor=models.ForeignKey('Vendor', on_delete=models.CASCADE,null=True)
#     order_date= models.DateField(auto_now_add=True,null=True)
#     location = models.CharField(max_length=10)
#     status=models.IntegerField(null=True)  

# class Redetail(models.Model):
#     redetail_id  = models.AutoField(primary_key=True)
#     reorder=models.ForeignKey('Orders', on_delete=models.CASCADE,null=True)
#     product=models.ForeignKey('Product', on_delete=models.CASCADE,null=True)
#     quantity = models.IntegerField()


# class Review(models.Model):
#     rid = models.AutoField(primary_key=True)
#     UserId=models.ForeignKey('Customer',on_delete=models.DO_NOTHING)
#     ProductId=models.ForeignKey('Product',on_delete=models.DO_NOTHING)
#     Rating = models.IntegerField()
#     Review = models.CharField(max_length=10)
#     Timestamp = models.DateTimeField(auto_now_add=True, blank=True)



  

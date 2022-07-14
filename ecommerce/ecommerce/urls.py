"""

Developed By : sumit kumar
facebook : fb.com/sumit.luv
Youtube :youtube.com/lazycoders


"""
from django.contrib import admin
from django.urls import path
from ecom import views
#from ecom import trail
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.home_view,name=''),
    
    path('logout', LogoutView.as_view(template_name='ecom/page-login.html'),name='logout'),

    
    
    path('logs', views.logs),
    path('logsin', views.logsin2),
    path('index', views.index),
    # path('shipper', views.shipper),
    # path('employ', views.employ),
    path('editprofile/<str:id>',views.editprofile),
    path('regs', views.regs),
    path('locationpage', views.locationpage),
    path('register', views.register2),
    path('resendotp/<email>', views.resendotp),
    path('otpverify', views.otpverify),
    path('indexs', views.indexs),
    path('profile', views.profile2),
    path('products', views.products),
    path('single/<str:pid>/<str:sid>', views.single2),
    #path('subcatsearch/<int:subid>', views.subcatsearch),
    path('subcatsearch/<str:subid>', views.subcatsearch2),
    path('pricefilter/<str:subid>/<int:p>', views.pricefilter),
    path('addtocart2', views.addtocart2),
    path('viewcart', views.viewcart2),
    path('removecart/<str:id>',views.removecart2),
    path('changepassword',views.changepassword),
    path('password/<int:id>',views.password),
    path('carts',views.carts),
    path('locations',views.locations),
    path('addlocation',views.addlocation),
    path('locationtype',views.locationtype),
    path('checkpin/<int:pin>',views.checkpin),
    path('addlocs',views.addlocs),
    # path('editlocation/<str:id>',views.editlocation),
    # path('deletelocation/<str:id>',views.deletelocation),
    path('selectlocation',views.selectlocation2),
    path('selectloc/<str:id>',views.selectloc2),
    path('pay',views.pay2),
    path('orders',views.orders2),
    path('order',views.order2),
    path('allorderdetails/<orderid>',views.allorderdetails),
    # path('cancelorder/<str:id>',views.cancelorder),
    path('removeaccount',views.removeaccount),
    path('report/<str:id>',views.report),
    # path('what',views.what),
    # path('orderstatus/<str:id>',views.orderstatus),
    path('payreport',views.payreport),
    path('corder',views.corder),
    path('trail',views.trail2),
    path('addwish/<pid>/<sid>',views.addwish),
    path('removewish/<pid>/<sid>',views.removewish),
    path('wishlist',views.wishlist),
    
    #path('auth', views.auth),

    path('adminlocations',views.adminlocations),
    path('adminpinset',views.adminpinset),
    path('adminaddlocations',views.adminaddlocations),
    path('disablepin/<pinid>',views.disablepin),
    path('enablepin/<pinid>',views.enablepin),
    path('adminlogs',views.adminlogs),
    path('adminlogout',views.adminlogout),
    path('adminlogin',views.adminlogin),
    path('adminindex',views.adminindex),
    path('adminhome',views.adminhome),
    path('adminpurchase',views.adminpurchase),
    path('adminpurchasedetails/<pid>',views.adminpurchasedetails),
    path('adminicons',views.adminicons),
    path('adminstock/<str:product_id>/',views.adminstock),
    path('adminproduct',views.adminproduct),
    path('adminvendor',views.adminvendor),
    path('admincustomer',views.admincustomer),
    path('productadd',views.productadd),
    path('addproduct',views.addproduct),
    path('addvendor',views.addvendor),
    path('insert',views.insertions),
    # path('editproduct/<str:proid>/',views.editproduct, name="editproduct"),
    # path('updateproduct/<str:proid>',views.updateproduct),
    path('disableproduct/<str:proid>',views.disableproduct),
    path('enableproduct/<str:proid>',views.enableproduct),
    path('disablereorder/<pid>',views.disablereorder),
    path('enablereorder/<pid>',views.enablereorder),
    path('disablestock/<str:sid>',views.disablestock),
    path('enablestock/<str:sid>',views.enablestock),
    path('adminbrand',views.adminbrand),
    path('addbrand',views.addbrand),
    path('addcategory',views.addcategory),
    path('addsubcategory',views.addsubcategory),
    path('editimages',views.editimages),
    path('editpage',views.editpage),
    path('adminorders',views.adminorders),
    path('adminorderdetails/<str:orderid>',views.adminorderdetails),
    path('reorderequest/<productid>',views.reorderequest),
    path('reorderequests',views.reorderequests),
    path('reorderconfirms',views.reorderconfirms),
    path('confirmreorders',views.confirmreorders),
    path('confirmsingle/<reorderid>',views.confirmsingle),
    path('cancelreorder/<reorderid>',views.cancelreorder),
    path('cancelvendoreorder/<reorderid>',views.cancelvendoreorder),
    path('viewsales',views.viewsales),
    path('monthsales/<int:month>',views.monthsales),
    path('a',views.sales),
    path('search',views.search),

    path('rating',views.rating),
    path('ordereport/<orderid>',views.ordereport),
    # path('adminorderdetails/link/<pdf:file>', views.pdfshow)

    path('', views.homepage, name='index'),
    # path('stockadd', views.stockadd),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('admin/', admin.site.urls),

    path('vlogout',views.vlogout),
    path('vlog',views.logs3),
    path('vregs',views.vregs),
    path('vpass/<id>',views.vpass),
    path('vendorpass',views.vendorpass),
    path('logsin3',views.logsin3),
    path('reorder',views.reorder),
    path('reordercheck',views.reordercheck),
    path('vendorindex',views.vendorindex),
    path('vendor',views.vendor),
    path('restock/<vendorid>',views.restock),
    path('vendorstoc',views.vendorstock),
    path('vendoradd',views.vendoradd),
    path('addprices',views.addprices),
    path('updatec/<p>/<int:q>',views.updatec),
    path('updates/<p>/<int:q>',views.updates),
    path('updatecc/<p>/<int:q>',views.updatecc),
    path('updatess/<p>/<int:q>',views.updatess),
    path('quantityupdate/<p>/<int:q>',views.quantityupdate),
    path('quantityupdateadmin/<p>/<int:q>',views.quantityupdateadmin),
    path('vendorpurchase',views.vendorpurchase),
    path('vpurchasedetails/<pid>',views.vpurchasedetails),
    path('vaddp',views.vaddp),
    path('vaddproduct',views.vaddproduct),
    path('vendorbrand',views.vendorbrand),
    path('vendorproduct',views.vendorproduct),
    path('vendorprofile',views.vendorprofile,name="vendorprofile"),

    path('editproduct/<str:proid>/',views.editproduct, name="editproduct"),
    path('updateproduct',views.updateproduct),
    path('vdisableproduct/<str:proid>',views.vdisableproduct),
    path('venableproduct/<str:proid>',views.venableproduct),
    
 
    path('recommendation',views.recommendation),

   


  


]

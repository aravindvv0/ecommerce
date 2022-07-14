from asyncio.windows_events import NULL
from email.policy import default

from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from matplotlib.collections import Collection
#from numpy import empty
from . import forms,models
from ecom.models import *
import random
from django.http import FileResponse, HttpResponseRedirect,HttpResponse,HttpResponseBadRequest
from django.core.mail import send_mail
#from django.contrib.auth.models import Group  
#from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
#from django.core.exceptions import ValidationError
#from django.core.validators import validate_email
from datetime import datetime
from reportlab.pdfgen import canvas
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage 
from firebase_admin import auth
import razorpay
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# from gcloud import storage
cred = credentials.Certificate("ecom/serviceAccountKey.json")
firebase_admin.initialize_app(cred,
{
    'storageBucket': 'e-commerce-a39dc.appspot.com'
}
)

db = firestore.client()

firebaseConfig = {

  "apiKey": "AIzaSyCGe3xUHXa2WnFKLienPi09Lr9J1a9ZhNA",
  "authDomain": "e-commerce-a39dc.firebaseapp.com",
  "databaseURL": "https://e-commerce-a39dc-default-rtdb.firebaseio.com",
  "projectId": "e-commerce-a39dc",
  "storageBucket": "e-commerce-a39dc.appspot.com",
  "messagingSenderId": "284810371785",
  "appId": "1:284810371785:web:3897088afb110ad7e1e318",
}
firebase=pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()




def trail(request):
        #accessing our firebase data and storing it in a variable
       
        db.collection('persons').add({'name':"john",'age':40})
        # name = database.child('Data').child('Name').get().val()
        # val = database.child('Data').child('Name').get().val()
        # stack = database.child('Data').child('Stack').get().val()
        # framework = database.child('Data').child('Framework').get().val()
        # main = database.child('Data').get().val()
        # data = database.child('Data').shallow().get().val()
        # uidlist=[]
        # ul = Customer.objects.all()
        # for i in data:
        #         uidlist.append(i)
        # print("hai")        
        # print(uidlist)        
        # email ="aa@gmail.com"
        # passs = "pass@14"
        
        
        #    # creating a user with the given email and password
        # user=authe.create_user_with_email_and_password(email,passs)
        # uid = user['localId']
        # context = {
        #     'name':val,
        #     'stack':stack,
        #     'framework':framework,
        #     'main':main,
        #     'uid':uid,
        #     'u':uidlist,
            

        # }  
        return render(request, 'ecom/a.html')
def trail2(request):
    # name = "Amazon"
    # num = 750
    # indices = ['ok','not ok',4]
    # today = datetime.now()
    # db.collection('NYSE').document('AMZN').set(
    #   {
    #     'name': name,
    #     'creationDate': today,
    #     'lastClose': num,
    #     'indices': indices
    #   }
    # )
    doc = db.collection('NYSE').document('AMZN').get()
    doc = doc.to_dict()
    docs = db.collection('persons').where('name', '==', 'Johnny').stream()
    for doc in docs:
        stock = doc.to_dict()
        print(stock["name"])
    return render(request, 'ecom/a.html')
def search(request):
    if request.session.is_empty():
        return redirect(logs)
    if request.method == 'POST':
        term = request.POST.get('query')
           
        data=[]

        product = db.collection('Product').where("name","==",term).get()
        for p in product:
            pro_ref=db.document("Product/"+p.id)
            pdict=p.to_dict()
            
            stock = db.collection('Stock').where("pro_refer","==",pro_ref).where("active","==","true").get()
            for s in stock:
                sdict = s.to_dict()
                sdict["id"]=s.id
                sdict["product_id"]=p.id
                res = sdict | pdict
                data.append(res)
            
          
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)   
    searchlist = searching()
    context={
        'datas':data,
        'cats':cats,
        'subcats':subcats,
        'search':searchlist
    }
        

    return render(request,'ecom/product.html',context)      
def logs(request):
    if request.session.get('id'):
        return redirect('/index')
    if request.session.get('adminid'):
        return redirect('/adminindex')    
    return render(request,'ecom/page-login.html')
def logs3(request):
    print("k")
    if request.session.get('id'):
        return redirect(vendor)
    return render(request,'vendor/page-login2.html')    
def carts(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    return render(request,'ecom/carts.html')    
def regs(request):
    return render(request,'ecom/reg.html')
#@login_required(login_url='/auth')     
def indexs(request):
    if not request.session.get('id'):
        return redirect('/logs')
    return render(request,'ecom/indexpage.html') 
# def auth(request):
#     if not request.session.get('id'):
#         return redirect('/logs')
#     value = request.GET.get('next')      
#     return HttpResponseRedirect(value)   
    #return HttpResponseRedirect(request.META['HTTP_REFERRER'])     
# def profile(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     id = request.session['id']
#     customer = Customer.objects.get(id=id)
#     return render(request,'ecom/profile.html',{"customer":customer,"name":customer.name})   
def profile2(request):
    if request.session.is_empty():
        return redirect(logs)
    id = request.session['id']
    c=db.collection("Customer").document(id).get()
    customer=c.to_dict()
    customer["customer_id"]=c.id
    context={"customer":customer}
    return render(request,'ecom/profile.html',context)     
def editprofile(request,id):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    if request.method=='POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        db.collection("Customer").document(id).update({"customer_name":name,"contact":mobile})
        messages.success(request,"Profile Updated")
        return HttpResponseRedirect('/profile')




def sess(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    a = request.session['email']
    return render(request,'ecom/a.html',{"a":a}) 
# def logsin(request):
#     if request.method=='POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         message="Invalid_Credinals"
#         count=Customer.objects.filter(email=email,password=password,active=1,role=1)
#         data = count.count()
#         if data == 1:
#             for c in count:
#                 id = c.id
#                 name=c.name
#                 #name = c.name
#             request.session['id']=id
#             request.session['name']=name
#             return HttpResponseRedirect('/index')
#         count=Customer.objects.filter(email=email,password=password,active=1,role=2)
#         data = count.count()
#         if data == 1:
#             for c in count:
#                 id = c.id
#                 name=c.name
#                 #name = c.name
#             request.session['id']=id
#             request.session['name']=name
#             return HttpResponseRedirect('/shipper') 
#         count=Customer.objects.filter(email=email,password=password,active=1,role=3)
#         data = count.count()
#         if data == 1:
#             for c in count:
#                 id = c.id
#                 name=c.name
#                 #name = c.name
#             request.session['id']=id
#             request.session['name']=name
#             return HttpResponseRedirect('/employ')       
#         return render(request,'ecom/page-login.html',{'message':message}) 

def logsin2(request):

    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        if email=="admin@admin.com" and password == "123456":
         try:
            login = authe.sign_in_with_email_and_password(email,password)
            uid = login['localId']
            request.session['adminid']=uid
            return HttpResponseRedirect('/adminindex')
         except:
            messages.error(request,"Invalid Credentials")
            return HttpResponseRedirect('/logs')    
        try:
            login = authe.sign_in_with_email_and_password(email,password)
            uid = login['localId']
            d=db.collection('Customer').where('userid','==',uid).where('active','==',"true").get()
            if len(d)==0:
                messages.error(request,"Account Disabled");
                return redirect(logs)
            else:    
             for i in d:
                # idict = i.to_dict()
                # if idict["role"]=='user':
                   request.session['id']=i.id
                   return HttpResponseRedirect('/index')
                # if idict["role"]=='vendor': 
                #    request.session['id']=i.id
                #    return HttpResponseRedirect(vendor)  

        except:
            messages.error(request,"Invalid Credentials")
            return HttpResponseRedirect('/logs')     

    return redirect('/logs')
def logsin3(request):

    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            login = authe.sign_in_with_email_and_password(email,password)
            uid = login['localId']
            print(uid)
            d=db.collection('Vendor').where('userid','==',uid).where('active','==',"true").get()
            if len(d)==0:
                messages.error(request,"Account Disabled");
                return redirect(logs3)
            else:    
             for i in d:
                idict = i.to_dict()
                print(idict['onetime'])
                if idict['onetime'] == 'on':
                    print(idict['onetime'])
                    return redirect(vpass, id = i.id)
                request.session['id']=i.id
                request.session['name']=idict["vname"]
                return redirect(vendor)
        except:
            messages.error(request,"Invalid Credentials")
            return redirect(logs3)     

    return redirect(logs3)
def vpass(request,id):
    context={'vendorid':id}

    return render(request,'vendor/vendorpass.html',context) 
    
def vendorpass(request):
    if request.method=='POST':
        npass = request.POST['npass']
        vendorid = request.POST['vendorid']
        udetails = db.collection('Vendor').document(vendorid).get().to_dict()
        uid = udetails["userid"]
        try:
            db.collection('Vendor').document(vendorid).update({
            'vpass':npass, 'onetime':'off' 
            })
            auth.update_user(
                uid,
                password=npass
            )
            request.session['id']=vendorid
            request.session['name']=udetails["vname"]
            return redirect(vendor)
        except:
            return redirect(logs3) 
    
def addvendor(request):
    return render(request,'home/addvendor.html')             
def adminlogs(request):
    if request.session.get('adminid'):
        return redirect('/adminindex')
    return render(request,'home/adminlogin.html')
def adminindex(request):
    return render(request,'home/index.html')
def adminlogin(request):

    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']
        if email=="admin@admin.com" and password == "123456":
         try:
            login = authe.sign_in_with_email_and_password(email,password)
            uid = login['localId']
            request.session['adminid']=uid
            return HttpResponseRedirect('/adminindex')

         except:
            messages.error(request,"Invalid Email or Password")
            return HttpResponseRedirect('/adminlogs') 
        else:
            messages.error(request,"Invalid Email or Password")
            return redirect('/adminlogs')         

    return redirect('/adminlogs')    


# def shipper(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     # shiporder = Orders.objects.filter(status=1)
#     shiporder = Orders.objects.select_related('customer','location').filter(status=1)
#     return render(request,"ecom/shipper.html",{"shiporder":shiporder})   
# def employ(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     employ = Orders.objects.select_related('customer','location').filter(status=4)
#     return render(request,"ecom/employ.html",{"employ":employ})          
def index(request):
       if request.session.is_empty():
        return render(request,'ecom/page-login.html')
       id = request.session['id']
       docs = db.collection('Customer').document(id).get()
       data = docs.to_dict()
       name = data['customer_name'] 
       request.session['name']=name
       searchlist=[] 
       search = db.collection('Product').get()
       for s in search:
           sd=s.to_dict()
           searchlist.append(sd["name"])  
       category = db.collection('persons').get()
       cats = []
       subcats = []
    
       for cat in category:
        catdict = cat.to_dict()
        catdict["id"]=cat.id
        cats.append(catdict)

        subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
        for sub in subcat:
            subdict = sub.to_dict()
            subdict["sub_id"]=sub.id
            subdict["cat_id"]=cat.id
            subcats.append(subdict)  
               
       context={'cats':cats,'subcats':subcats,'search':searchlist}    
       return render(request,'ecom/indexpage.html',context)


            
        # try:
        #     validate_email(a)
        #     return render(request,'ecom/indexpage.html',{"a":a})
        # except ValidationError:
        #     c = "Invalid Email"
        #     return render(request,'ecom/page-login.html',{"c":c})
        

# def register(request):
#     if request.method=='POST':
#         email = request.POST['email']
#         password = request.POST['pswd']
#         name = request.POST['name']
#         mobile = request.POST['phno']
#         data = Customer.objects.filter(email=email).count()
#         if  data == 0:
#             user = Customer.objects.create(email=email,password=password,mobile=mobile,name=name,active=1,role=1)
#             user.save()
#             messages.success(request,("Registration Successful"))
#             return HttpResponseRedirect('/logs')
#         messages.error(request,("Email"))    
#         return render(request,'ecom/reg.html')    
#     return render(request,'ecom/reg.html')

def vregs(request):
    if request.method=='POST':
        
        vemail = request.POST['vemail']
        vname = request.POST['vname']
        vcontact = request.POST['vcontact']
        vaddress=request.POST['vaddress']
        today = datetime.now()

        try:    
            generate_random = random.randint(111111,999999)
            generate_random = str(generate_random)
            user=authe.create_user_with_email_and_password(vemail,generate_random)
            #link=authe.generate_email_verification_link(email, action_code_settings=None)
           
            email_from = settings.EMAIL_HOST_USER
            res = send_mail("Big Shope Vendor Registartion, Use This Password to Sign in : ", generate_random, email_from, [vemail])
            # generate_random = int(generate_random)
            uid = user['localId']
        except:
            messages.error(request,("Email Already Exists"))
            return redirect('/addvendor')    
        
        today = datetime.now()
        db.collection('Vendor').add(
            {
             'vname': vname,
             'registerDate': today,
             'userid':uid,
             'vcontact': vcontact,
             'vemail':vemail,
             'vaddress':vaddress,
             'vpass':generate_random,
             'active':"true",
             'onetime':'on',
             'role':'vendor'
            }
            )
      
        #return HttpResponseRedirect('/logs') 
        return redirect(adminhome) 
def register2(request):
    if request.method=='POST':
        
        email = request.POST['email']
        password = request.POST['pswd']
        name = request.POST['name']
        mobile = request.POST['phno']
        today = datetime.now()
        try:    
            user=authe.create_user_with_email_and_password(email,password)
            #link=authe.generate_email_verification_link(email, action_code_settings=None)
            generate_random = random.randint(111111,999999)
            generate_random = str(generate_random)
            email_from = settings.EMAIL_HOST_USER
            res = send_mail("Big Shope Registartion OTP", generate_random, email_from, [email])
            generate_random = int(generate_random)
            uid = user['localId']
        except:
            messages.error(request,("Email Already Exists"))
            return render(request,'ecom/reg.html')    
        
        today = datetime.now()
        db.collection('Customer').add(
            {
             'customer_name': name,
             'creationDate': today,
             'userid':uid,
             'contact': mobile,
             'email':email,
             'password':password,
             'active':"false",
             'role':'user'
            }
            )
      
        #return HttpResponseRedirect('/logs') 
        return render(request,'ecom/verifymail.html',{'email':email,'generate_random':generate_random})         
def resendotp(request,email):
     generate_random = random.randint(111111,999999)
     generate_random = str(generate_random)
     email_from = settings.EMAIL_HOST_USER
     res = send_mail("Big Shope Registartion OTP", generate_random, email_from, [email])
     generate_random = int(generate_random)      
     return render(request,'ecom/verifymail.html',{'email':email,'generate_random':generate_random})
def otpverify(request):
    if request.method=='POST':
        otp = request.POST['otp']
        originalotp = request.POST['originalotp']
        otp = int(otp)
        originalotp = int(originalotp)
        email = request.POST['email']
        if otp == originalotp:
           user = db.collection('Customer').where('email','==',email).get()
           for u in user:
               db.collection('Customer').document(u.id).update({'active':'true'})
           messages.success(request,("Registration Successful"))     
           return redirect(logs) 
        else:
            messages.success(request,("Wrong OTP"))     
            return render(request,'ecom/verify.html')    
        

def locationpage(request):
    return render(request,'ecom/addlocation.html')
def searching():
    searchlist=[] 
    search = db.collection('Product').get()
    for s in search:
           sd=s.to_dict()
           searchlist.append(sd["name"])
    return searchlist
#@login_required(login_url='/logs')
def products(request):
    if request.session.is_empty():
        return redirect(logs)
    searchlist = searching()
    docs = db.collection('Stock').where('active','==','true').get()
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)
    
    # context = {'datas': [doc.id,doc.to_dict() for doc in docs]}
    data=[]
    for doc in docs:
        
       dock= doc.to_dict()
      
       dock["id"]=doc.id
       pro=dock["pro_refer"].get()
       prosid = pro.id
       prod = pro.to_dict()
       prod["product_id"]=prosid
       res = dock | prod
       data.append(res)
      
         
    print(data)
    
    # for d in do:
    #    docs = db.collection('Product').document(d).stream()
    #    data.append(d.id,docs.to_dict())

    # for doc in docs:
        
    #     data.append(doc.to_dict())

  
    
        
    #docs = db.collection('persons').where('name', '==', 'Johnny').stream()
    # datas = Product.objects.all().filter(active=1)
    # category = Category.objects.all().filter(active=1)
    # subcategory = Subcategory.objects.all().filter(active=1)
  
    hide=1
    return render(request,'ecom/product.html',{'datas':data,'cats':cats,'subcats':subcats,'hide':hide,'search':searchlist})
    
# def single(request,pid):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     id = request.session['id']
#     customer = Customer.objects.get(id=id)
#     category = Category.objects.all().filter(active=1)
#     subcategory = Subcategory.objects.all().filter(active=1)
#     products=Product.objects.get(id=pid)
#     stocks=Stock.objects.filter(product_id=pid)
#     stockleft=0
#     for stock in stocks:
#         stockleft=stockleft+stock.quantity
#     return render(request,'ecom/single.html',{"products": products,"stockleft":stockleft,"category":category,"subcategory":subcategory,"name":customer.name})

def single2(request,pid,sid):
    if request.session.is_empty():
        return redirect(logs)
    docs = db.collection('Product').document(pid).get()
    #context = {'datas': [doc.id,doc.to_dict() for doc in docs]}

    docs = docs.to_dict()
    sub = docs["subcategory"].get().to_dict()
    # aa = str(docs["cat"])
    # aa=str(aa)
    # cat = db.collection('persons').document(aa).collection('subcategory').document(docs["sub"]).get()
    # print(cat.to_dict())
    stock = db.collection('Stock').document(sid).get()
    stocks = stock.to_dict()
    stocks["id"]=stock.id
   
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict) 

    cus_rate = request.session['id']
    rateid = db.document('Customer/'+cus_rate)
    proid =  db.document('Product/'+pid)
    orderstatus = 0
    orderid=db.collection('Orders').where('cus_order','==',rateid).get()
    for order in orderid:
        orderef = db.document('Orders/'+order.id)
        a=db.collection('Orderdetails').where('orderid','==',orderef).where('orderproduct','==',proid).get()
        if a != None:
            orderstatus = 1

    print(orderstatus)
    rating = db.collection('Rating').where('cus_rating','==',rateid).where('pro_rating','==',proid).get() 
    ratdict = {} 
    ratingid=0
    for rat in rating:
        ratingid = rat.id
        ratdict = rat.to_dict()
    res = not ratdict
    ratelist=[]
    allratings = db.collection('Rating').where('pro_rating','==',proid).get()
    for allrating in allratings:
        allratingdict = allrating.to_dict()
        customerd=allratingdict['cus_rating'].get().to_dict()
        result=allratingdict | customerd
        ratelist.append(result)

    wish = db.collection('Wishlist').where('cref','==',rateid).where('pref','==',proid).get()
    mywish = 0
    for w in wish:
        wd = w.to_dict()
        mywish=1
    searchlist = searching()    
    context = {'orderstatus':orderstatus,'products':docs,'sub':sub,'cats':cats,'subcats':subcats,'stock':stocks,'pid':pid,'sid':sid,'rating':ratdict,'res':res,'ratingid':ratingid,
    'rlist':ratelist,'mywish':mywish,'search':searchlist}
    return render(request,'ecom/single.html',context)

    

                      

# def subcatsearch(request,subid):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     data=Product.objects.filter(scatid_id=subid,active=1)
#     category = Category.objects.all()
#     subcategory = Subcategory.objects.all()
#     id = request.session['id']
#     customer = Customer.objects.get(id=id)
#     return render(request,'ecom/product.html',{"datas": data,"category":category,"subcategory":subcategory,"name":customer.name})

def subcatsearch2(request,subid):
    if request.session.is_empty():
        return redirect(logs)
    data=[]
    category = db.collection('persons').get()
    for c in category:
        subcategory = db.collection('persons').document(c.id).collection('subcategory').document(subid).get().to_dict()
        print(subcategory)
        if subcategory==None:
             pass
        else:
            categoryid = c.id
            break  
    print(categoryid)      
    sub_ref = db.document('persons/'+categoryid+'/subcategory/'+subid)    
    print(sub_ref)
    product = db.collection('Product').where("subcategory","==",sub_ref).where("active","==","true").get()
    for p in product:
        pro_ref=db.document("Product/"+p.id)
        pdict=p.to_dict()
        
        stock = db.collection('Stock').where("pro_refer","==",pro_ref).where("active","==","true").get()
        for s in stock:
            sdict = s.to_dict()
            sdict["id"]=s.id
            sdict["product_id"]=p.id
            res = sdict | pdict
            data.append(res)
            
          
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)   
    hide=0
    searchlist = searching()
    context={
        'datas':data,
        'cats':cats,
        'subcats':subcats,
        'subid':subid,'hide':hide,
        'search':searchlist
    }
    return render(request,'ecom/product.html',context)    
def pricefilter(request,subid,p):
    if request.session.is_empty():
        return redirect(logs)
    data=[]
    category = db.collection('persons').get()
    for c in category:
        subcategory = db.collection('persons').document(c.id).collection('subcategory').document(subid).get().to_dict()
        print(subcategory)
        if subcategory==None:
             pass
        else:
            categoryid = c.id
            break  
    print(categoryid) 

    price1 = 0
    price2 = 0
    if p == 1:
        price1=0
        price2=100 
    if p == 2:
        price1 = 100
        price2=1000  
    if p == 3:
        price1 = 1000
        price2=10000  
    if p == 4:
        price1 = 10000
        price2=30000
    if p == 5:
        price1 = 30000
        price2=50000 
    if p == 6:
        price1 = 50000
        price2=100000 
    if p == 7:
        price1 = 100000
        price2=200000 
    if p == 8:
        price1 = 200000
        price2=500000                          

    sub_ref = db.document('persons/'+categoryid+'/subcategory/'+subid)    
    print(sub_ref)
    product = db.collection('Product').where("subcategory","==",sub_ref).where("active","==","true").get()
    for p in product:
        pro_ref=db.document("Product/"+p.id)
        pdict=p.to_dict()
        
        stock = db.collection('Stock').where("pro_refer","==",pro_ref).where("active","==","true").where('price','>=',price1).where('price','<',price2).get()
        for s in stock:
            sdict = s.to_dict()
            sdict["id"]=s.id
            sdict["product_id"]=p.id
            res = sdict | pdict
            data.append(res)
            
          
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)   
    hide=0
    context={
        'datas':data,
        'cats':cats,
        'subcats':subcats,
        'subid':subid,'hide':hide
    }
    return render(request,'ecom/product.html',context)     

# def addtocart(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     if request.method=='POST':
#         productid = request.POST['productid']
#         quantity = request.POST['quantity']
#         quantity = int(quantity)
#         data = Product.objects.get(id=productid)
#         pid = productid
#         customerid =  request.session["id"]
#         unitprice = float(data.price)
#         totalprice = quantity*unitprice
#         avails = Stock.objects.filter(product_id=productid)
#         availablestock  = 0
#         for avail in avails:
#             availablestock = availablestock+avail.quantity
#         if availablestock < quantity:
#             messages.success(request, ("Out of Stock"))
#             return redirect(single, pid = pid)   
        
#         user = Cart.objects.create(customer_id=customerid,productid_id=productid,unitprice=unitprice,quantity=quantity,totalprice=totalprice)
#         user.save()
#         #stocks = Stock.objects.filter(product_id=productid).order_by('id').exclude("expirydate"==NULL)
#         stocks = Stock.objects.filter(product_id=productid).order_by('expirydate')
        
#         #minexpiry=datetime.strptime(minexpiry,'%y-%m-%d').date()
#         for stock in stocks:
#             if stock.quantity < quantity:
#                 # request.session['stock']=[]
#                 # request.session['stock']['stockid']=stock.id
#                 # request.session['stock']['quan']=stock.quantity
#                 quantity = quantity-stock.quantity 
#                 stock.quantity = 0
#                 stock.save()
#             if stock.quantity > quantity:
#                 # request.session['stock']=[]
#                 # request.session['stock']['stockid']=stock.id
#                 # request.session['stock']['quan']=stock.quantity
#                 stock.quantity = stock.quantity-quantity
#                 stock.save()
#                 break
#             if stock.quantity == quantity:
#                 stock.quantity = stock.quantity-quantity
#                 stock.save()
#                 break
#         return redirect(single, pid = pid)

def addtocart2(request):
    if request.session.is_empty():
        return redirect(logs)
    if request.method=='POST':
        stockid = request.POST['stockid']
        quantity = request.POST['quantity']
        stocked = db.collection('Stock').document(stockid).get()
        stockdetails=stocked.to_dict()
        productdetails = stockdetails["pro_refer"].get()
        productid = productdetails.id
        customerid =  request.session["id"]
        stockdetails=stocked.to_dict()
        quantity = int(quantity)
        currentquantity = stockdetails["quantity"]
        currentquantity=int(currentquantity)
        if quantity > currentquantity:
            messages.success(request, ("Out of Stock"))
            return redirect(single2, pid = productid, sid= stockid)
        unitprice = stockdetails["price"]
        totalprice = unitprice * quantity
        # if totalprice > 20000:    
        #     messages.success(request, ("20000 is transaction limit"))
        #     return redirect(single2, pid = productid, sid= stockid)
        cus_ref=db.document('Customer/'+customerid)
        stock_ref=db.document('Stock/'+stockid)
        alreadyadded=db.collection('Cart').where('cus_ref','==',cus_ref).where('pro_ref','==',stockdetails["pro_refer"]).get()
        print(alreadyadded)
        if alreadyadded != []:
            for added in alreadyadded:
                addict = added.to_dict()
                currentquant=addict["quantity"]
                addquantity = currentquant + quantity
                addtotalprice = addquantity * addict['unitprice']
                db.collection('Cart').document(added.id).update({'quantity':addquantity,'totalprice':addtotalprice})
        else:        
            db.collection('Cart').add({'product_id':productid,'stocknumber':stock_ref,'quantity':quantity,'cus_ref':cus_ref,'stock_ref':stock_ref,'pro_ref':stockdetails["pro_refer"],'totalprice':totalprice,'unitprice':unitprice})
        
        newq = currentquantity-quantity  
        db.collection('Stock').document(stockid).update({'quantity':newq})
        newstock = db.collection('Stock').document(stockid).get().to_dict()
        # if newstock["quantity"]==0:
        #     db.collection('Stock').document(stockid).update({'active':'false'})
        messages.success(request,"Added to Cart")    
        return redirect(single2, pid = productid, sid = stockid)        

def foreignt(request):
    
    p=db.collection('Product').document('iphone').get()
    s=db.collection('Customer').document('zrMlNdAhRB96Wrw52usp').get()

    pd=p.to_dict()
    sd=s.to_dict()
    print(pd)
    print(sd)
    res = pd | sd
    print(res)
    return render(request,'ecom/a.html')        
# def viewcart(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     customerid = request.session["id"] 
#     customer = Customer.objects.get(id=customerid)
#     cartlist = Cart.objects.filter(customer_id=customerid)
#     amount=0
#     ptlist = Product.objects.all()
#     for cart in cartlist:
#         amount = amount + cart.totalprice
#     return render(request,'ecom/cart.html',{"cartlist": cartlist, "amount":amount,"ptlist":ptlist,"name":customer.name})
def viewcart2(request):
    if request.session.is_empty():
        return redirect(logs)   
    customerid = request.session["id"] 
    cusid=db.document("Customer/"+customerid)
    cart=db.collection('Cart').where("cus_ref","==",cusid).get()
    cartlist=[]
    amount=0
    for c in cart:
        cdict = c.to_dict()
        cdict["cart_id"]=c.id
        cusdetail = cdict["cus_ref"].get()
        cusdict = cusdetail.to_dict()
        cusdict["customer_id"] = customerid

        pdetail = cdict["pro_ref"].get()
        pdict = pdetail.to_dict()
        amount = amount + cdict["totalprice"]
        res = cdict|pdict|cusdict
        cartlist.append(res)
    print(cartlist)    
    context={'cartlist':cartlist,'amount':amount}    
    return render(request,'ecom/cart.html',context)    
# def removecart(request,id):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     cart = Cart.objects.get(id=id)
#     quantity = cart.quantity
#     stocks = Stock.objects.filter(product_id=cart.productid).order_by('expirydate')
#     cart.delete()
#     for stock in stocks:
#         stock.quantity=stock.quantity+quantity
#         stock.save()
#         break
#     return redirect('/viewcart')

def removecart2(request,id):
    if request.session.is_empty():
        return redirect(logs)
    cart = db.collection('Cart').document(id).get().to_dict()
    quantity=cart["quantity"]
    stock=cart["stock_ref"].get().to_dict()
    
    stockquantity=stock["quantity"]
    totalquantity = stockquantity + quantity
    cart["stock_ref"].update({"quantity":totalquantity})
    db.collection('Cart').document(id).delete()
    return redirect(viewcart2)    


# def changepassword(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     id = request.session['id']
#     customer = Customer.objects.get(id=id)
#     return render(request,'ecom/changepassword.html',{"customer":customer,"name":customer.name}) 




# def order(request,customerid):
#     cart = Cart.objects.filter(customer_id=customerid)
    #order = Order.create(customerid, amount, status,locationid, orderdate, deliveydate)
    #orderdetails = Orderdetails.create(orderid, productid, quantity, unitprice , totalprice, )
    #remove from cart
    #update stock
    #expiry issue

def locations(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    
    return render(request,'ecom/locations.html')

# def selectlocation(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     id=request.session['id']
#     location = Location.objects.filter(customer_id=id)
#     return render(request,'ecom/selectlocation.html',{'location':location})
def locationtype(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    pinlist=[]
    pins=db.collection('Pin').get() 
    for p in pins:
        pinlist.append(p.id)    
    context={'pins':pinlist}      
    return render(request,'ecom/locationtype.html',context)  
def checkpin(request, pin):
    p = str(pin)
    pin = int(pin)
    location = db.collection('Pin').where('pin','==',pin).where('active','==','true').get()
    if location == []:
            messages.success(request,"Delivery not available to this location")
            return redirect(locationtype)
    else:
       for loc in location:
          locdict = loc.to_dict()  
       pinlist=[]
       pins=db.collection('Pin').get() 
       for p in pins:
          pinlist.append(p.id)             
       context = {'a':locdict,'pins':pinlist}    
       return render(request,'ecom/locationtype.html',context)
    #return redirect(products)      
def addlocs(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    id=request.session['id']
    customer_ref = db.document('Customer/'+id)
    if request.method=='POST':
        address = request.POST.get('address')
        district = request.POST.get('district')
        print(district)
        city = request.POST.get('city')
        pin = request.POST['pin']
        locid = 0
        a=db.collection('Location').where('pin','==',pin).where('address','==',address).get()
        if a == []:
            print("add")
            b= db.collection('Location').add({
            'address':address,
            'city':city,
            'pin':pin,
            'district':district,
            'cus_loc':customer_ref
                                            })
            locid = b[1].id
        else:
            for i in a:
                print(i)
                locid = i.id
        print(locid)
        return redirect(selectloc2,id=locid)
    
   
def selectlocation2(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    id=request.session['id']
    cusid=db.document("Customer/"+id)
    location=db.collection('Location').where("cus_loc","==",cusid).get()
    locationlist=[]
    for l in location:
        locdict = l.to_dict()
        locdict["locationid"] = l.id
        locationlist.append(locdict)
    print(locationlist)  
    context = {"location":locationlist}  
    return render(request,'ecom/selectlocation.html',context)
# def selectloc(request, id):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     data = Location.objects.select_related('customer').filter(id=id)
#     id=request.session['id']
#     pay = Payment.objects.filter(customer_id=id)
#     return render(request,'ecom/payment.html',{'data':data,'pay':pay})
def selectloc2(request, id):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    customerid = request.session["id"] 
    cusid=db.document("Customer/"+customerid)
    cartitems=db.collection('Cart').where("cus_ref","==",cusid).get()
    amount=0
    for cart in cartitems:
        cartdict = cart.to_dict()
        amount=amount+cartdict["totalprice"]
    amount=int(amount)   
    if amount > 20000:
       messages.error(request,"Can't order for more than Rs 20000")
       return redirect(viewcart2)  
    try:    
        location=db.collection('Location').document(id).get()
        locationdict = location.to_dict()
        locationdict["locationid"] = id
        customer = locationdict["cus_loc"].get().to_dict()
        customerid=request.session['id']
        cusid=db.document('Customer/'+customerid)
        customer["customerid"] = customerid
        data = customer | locationdict
        
        # pay = Payment.objects.filter(customer_id=id)
        pay=10
        cartitems=db.collection('Cart').where("cus_ref","==",cusid).get()
        amount=0
        for cart in cartitems:
            cartdict = cart.to_dict()
            print(cartdict)
            amount=amount+cartdict["totalprice"]
        currency = 'INR'
        
        amount = amount*100
        
        amount = amount  # Rs. 200
        print(amount)
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                        currency=currency,
                                                        payment_capture='0'))
        print(amount)
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/paymenthandler/'
        print(amount)
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context["data"]=data
        response=render(request,'ecom/payment.html',context=context)
        response.set_cookie('location', id)
        return response
    except:
        return redirect(order2)    
def addlocation(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    id=request.session['id']
    customer_ref = db.document('Customer/'+id)
    if request.method=='POST':
        address = request.POST['address']
        district = request.POST['district']
        city = request.POST['city']
        pin = request.POST['pin']
        db.collection('Location').add({
            'address':address,
            'city':city,
            'pin':pin,
            'district':district,
            'cus_loc':customer_ref
        })
        return redirect('/locations')
# def editlocation(request,id):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     location = Location.objects.get(id=id)
#     if request.method=='POST':
#         address = request.POST['address']
#         district = request.POST['district']
#         city = request.POST['city']
#         pin = request.POST['pin']
#         location.address=address
#         location.pin = pin
#         location.city=city
#         location.district=district
#         location.save()
#         return redirect('/locations')        
# def deletelocation(request,id):
#      if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#      location = Location.objects.get(id=id)
#      location.active=0
#      location.save()
#      return redirect('/locations')
# def reordercheck(orderid):
#     Reorder = ()
#     orderdetails = Orderdetails.objects.filter(order_id=orderid)
#     l = []
#     for o in orderdetails:
#       l.append(o.product_id) 
#     stockleft=0    
#     for i in (0,len(l)):
#         stocks=Stock.objects.filter(product_id=i)
#         for stock in stocks:
#            stockleft=stockleft+stock.quantity 
#            if(stockleft<100):
#                 p = Product.objects.get(id=i)
#                 vendor = p.vendor_id
#                 reorder = Reorder.objects.create(location="BigShope Warehouse",status=1,vendor_id=vendor)
#                 reorder.save()
#                 redetail = Redetail.objects.create(quantity=1000,product_id=i,reorder=Reorder)
#                 redetail.save()
#                 return True;
#            else:
#                 return True;

 
def pay(request):
    if request.session.is_empty():
        return redirect(logs)
    if request.method=='POST':
        locid=request.POST['locid']
        paymentid= str(random.randint(11111111, 99999999))
        T = "T"
        payment = T + paymentid
        # paymenidt="T1626252625"

        
        status2="Ordered"
        customerid = request.session["id"] 
        cusid=db.document("Customer/"+customerid)
        loc_id=db.document("Location/"+locid)
        cartitems=db.collection('Cart').where("cus_ref","==",cusid).get()
        cartlist=[]

        amount=0
        for cart in cartitems:
            cartdict = cart.to_dict()
            amount=amount+cartdict["totalprice"]

        orderdate = datetime.today()
        
        orders=db.collection('Orders').add({'cus_order':cusid,'loc_order':loc_id,'amount':amount,'orderdate':orderdate,'deliver_date':orderdate,'order_status':status2,'active':'true'})
       
        orderid = db.document("Orders/"+orders[1].id)
      
        for cart in cartitems:
            cartdict = cart.to_dict()
            orderdetails= db.collection('Orderdetails').add({'orderid':orderid,'orderproduct':cartdict["pro_ref"],'orderstock':cartdict["stocknumber"],'quantity':cartdict["quantity"],'unitprice':cartdict["unitprice"],'totalprice':cartdict["totalprice"]})
           
        for cart in cartitems:
            db.collection('Cart').document(cart.id).delete()
        #     cart.delete()
        # # buffer = io.BytesIO()
        # reordercheck(orderid) 
        # for o in orders:
        #     orderid=o.order_id
        #     break
        # ordering = Orders.objects.get(order_id=orderid)
        # locationing = Location.objects.get(id=ordering.location_id)
        # customering = Customer.objects.get(id=ordering.customer_id)
        # orderdetails = Orderdetails.objects.filter(order_id=orderid)

        # response = HttpResponse(content_type='application/pdf') 
        # response['Content-Disposition']='attachment;filename="file.pdf"'
        # p = canvas.Canvas(response)

        # p.drawString(240,800,"Big Shope")
        # p.drawString(300,780,"     ")
        # p.drawString(230,760,"Purchase Receipt")
        # p.drawString(300,750,"     ")
        # p.drawString(230,720,"Or"+str(ordering.order_date)+str(ordering.order_id))  
      
        # p.drawString(100,660,"Name:                               Transcation id                           Order date")
        # p.drawString(100,640,".............................................................................................................")
        
        # p.drawString(100,620,customering.name + "                         "+ordering.payment+"                              "+str(ordering.order_date))
        # p.drawString(60,560,"Delivery address:     "+locationing.address + " "+ locationing.city + " "+ locationing.district+", "+str(locationing.pin))
        # p.drawString(240,520,"Products : ")
        # i=100
        # j=460
        # for ors in orderdetails:
        #     producting = Product.objects.get(id=ors.product_id)
        #     p.drawString(i,j,producting.name+" \n   Quantity :  " + str(ors.quantity)+ " \n Unit Price : "+ str(ors.unitprice)+" \n Subtotal : "+ str(ors.totalprice))
        #     j=j-40


      
        # p.drawString(180,j-40,"Inclusive of all taxes  Total Amount :    "+str(ordering.amount))

        # p.drawString(160,j-100,'http://127.0.0.1:8000/payreport')


        # p.showPage()
        # p.save()
        # #messages.success(request, ("Order Successful")) 
        # # feed = Feedback.objects.create(filepath="file.pdf")
        # # feed.save()
        
        # return FileResponse(response,content_type='application/pdf')
        
        # #return FileResponse(buffer,as_attachment=True,filename="hello.pdf")
        return redirect('/order')    
    return redirect('/order')
def pay2(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    # if request.method=='POST':
        # locid=request.POST['locid']
        # paymentid= str(random.randint(11111111, 99999999))
        # T = "T"
        # payment = T + paymentid
        # paymentid="T1626252625"

        
    status2="Ordered"
    customerid = request.session["id"] 
    cusid=db.document("Customer/"+customerid)
    
    cartitems=db.collection('Cart').where("cus_ref","==",cusid).get()
    cartlist=[]

    amount=0
    for cart in cartitems:
        cartdict = cart.to_dict()
        amount=amount+cartdict["totalprice"]
    amount=int(amount)   
    if amount > 20000:
       return redirect(viewcart2)
    orderdate = datetime.today()
    location=request.COOKIES['location']
    print(location)
    loc_id=db.document("Location/"+location)
    roid=request.COOKIES['razorpay_order_id']
    print(roid)
    poid=request.COOKIES['razorpay_payment_id']
    print(poid)

    orders=db.collection('Orders').add({'cus_order':cusid,'loc_order':loc_id,'amount':amount,'orderdate':orderdate,'deliver_date':orderdate,'order_status':status2,'pay_orderid':roid,'payment_id':poid,'active':'true'})
    
    orderid = db.document("Orders/"+orders[1].id)
    a=redirect(ordereport,orderid=orders[1].id)
    a.delete_cookie('location')
    a.delete_cookie('razorpay_order_id')
    a.delete_cookie('razorpay_payment_id')
    for cart in cartitems:
        cartdict = cart.to_dict()
        ordersdetails= db.collection('Orderdetails').add({'orderid':orderid,'orderproduct':cartdict["pro_ref"],'orderstock':cartdict["stocknumber"],'quantity':cartdict["quantity"],'unitprice':cartdict["unitprice"],'totalprice':cartdict["totalprice"]})
        
    for cart in cartitems:
        db.collection('Cart').document(cart.id).delete()
    reordercheck(orders[1].id)   
    return a
    # return redirect(ordereport)
    #     ordering = db.collection('Orders').document(orders[1].id).get().to_dict()
    #     locationing = db.collection('Location').document(locid).get().to_dict()
    #     customering = db.collection('Customer').document(customerid).get().to_dict()
    #     orderdetails = db.collection('Orderdetails').where('orderid','==',orderid).get()

    #     response = HttpResponse(content_type='application/pdf') 
    #     # response['Content-Disposition']='attachment;filename="file.pdf"'
    #     p = canvas.Canvas(response)

    #     p.drawString(240,800,"Big Shope")
    #     p.drawString(300,780,"     ")
    #     p.drawString(230,760,"Purchase Receipt")
    #     p.drawString(300,750,"     ")
    #     p.drawString(230,720,"Or"+str(ordering["orderdate"])+str(orders[1].id))  
      
    #     p.drawString(100,660,"Name:                               Transcation id                           Order date")
    #     p.drawString(100,640,".............................................................................................................")
        
    #     p.drawString(100,620,customering["customer_name"] + "                         "+payment+"                              "+str(ordering["orderdate"]))
    #     p.drawString(60,560,"Delivery address:     "+locationing["address"] + " "+ locationing["city"] + " "+ locationing["district"]+", "+str(locationing["pin"]))
    #     p.drawString(240,520,"Products : ")
    #     i=100
    #     j=460
    #     for ordict in orderdetails:
    #         ors = ordict.to_dict()
    #         producting = ors["orderproduct"].get().to_dict()
    #         p.drawString(i,j,producting["name"]+" \n   Quantity :  " + str(ors["quantity"])+ " \n Unit Price : "+ str(ors["unitprice"])+" \n Subtotal : "+ str(ors["totalprice"]))
    #         j=j-40


      
    #     p.drawString(180,j-40,"Inclusive of all taxes  Total Amount :    "+str(ordering["amount"]))

    #     p.drawString(160,j-100,'http://127.0.0.1:8000/payreport')


    #     p.showPage()
    #     p.save()
    #     #messages.success(request, ("Order Successful")) 
    #     # feed = Feedback.objects.create(filepath="file.pdf")
    #     # feed.save()
        
    #     return FileResponse(response,content_type='application/pdf')
        
        #return FileResponse(buffer,as_attachment=True,filename="hello.pdf")    #
def reordercheck(orderid):
    #orderid="DGt9q6bGZ7y09Qo9uCeE"
    orderref = db.document('Orders/'+orderid)
    stockcount = 0
    productlist=[]
    reorderquantity=1000
    date=datetime.now()
    orderdetails=db.collection('Orderdetails').where('orderid','==',orderref).get()
    for o in orderdetails:
        odict = o.to_dict()
        productlist.append(odict['orderproduct'].get().id)
       
    print(productlist) 
    for p in productlist:
        
        pro_refer = db.document('Product/'+p)

        pv = db.collection('Product').document(p).get().to_dict()
        if pv["reorder"]=='active':
            stockdetails = db.collection('Stock').where('pro_refer','==',pro_refer).where('active','==','true').get()
            for sdict in stockdetails:
                s=sdict.to_dict()
                stockcount = stockcount + s["quantity"]
            print(stockcount)
        

            if stockcount < 50:
                    stocks=db.collection('Stock').order_by('purchase_date',direction=firestore.Query.DESCENDING).limit(1).where("pro_refer","==",pro_refer).where('active','==','true').get()   
                    for st in stocks:
                        stock_ref=db.document('Stock/'+st.id)
                        stdict = st.to_dict()
                        vprice=db.collection('Vendorstock').document(p).get().to_dict()
                        db.collection('Reorder').add({'reorder_status':'Not confirmed','vendor_ref':pv["vendor"],'product_ref':pro_refer,'stock_ref':stock_ref,'reorder_date':date,
                        'reorderquantity':reorderquantity,'purchase_price':vprice['cprice'],'selling_price':vprice["sprice"]})
    return
        

def reorder(reqest):
    
    stockid="F2CbKgNyjVSjkWJcGLSM"
    productid="iphone"
    stock_ref=db.document('Stock/'+stockid)
    pro_ref=db.document('Product/'+productid)
    stocks=db.collection('Stock').order_by('purchase_date',direction=firestore.Query.DESCENDING).limit(1).where("pro_refer","==",pro_ref).get()
    #stock = stocks.where("pro_refer","==",pro_ref).get()
    reorderquantity=1000
    date=datetime.now()
    for s in stocks:
        if s.id==stockid:
            sdict = s.to_dict()

            db.collection('Reorder').add({'reorder_status':'Not confirmed','vendor_ref':sdict["vendor"],'product_ref':pro_ref,'stock_ref':stock_ref,'reorder_date':date,
            'reorderquantity':reorderquantity,'purchase_price':sdict['cost_price'],'selling_price':sdict["price"]})
            
        else:
            pass   
    return redirect(logs)
def vendor(request):
    if request.session.is_empty():
        return redirect(logs3)
    id=request.session['id']
    vendor=db.document('Vendor/'+id)
    reorder = db.collection('Reorder').where("vendor_ref","==",vendor).where('reorder_status','==','Confirmed').get()
    reorderlist=[]
    for r in reorder:
        a = r.to_dict()
        a["rid"]=r.id
        product = a["product_ref"].get()
        productdict = product.to_dict()
        productdict["productid"]=product.id
        if a["stock_ref"]==0:
            res = a  | productdict
        else:    
            stock =  a["stock_ref"].get()
            stockdict = stock.to_dict()
            stockdict["stockid"]=stock.id
            res = a | stockdict | productdict

        reorderlist.append(res)
    context={'stock':reorderlist,'vendorid':id} 
    print(reorderlist)   
    return render(request,'vendor/vendorindex.html',context)  
def vendorindex(request):

    return render(request,'vendor/vendorindex.html')
def restock(request,vendorid):
    vendor=db.document('Vendor/'+vendorid)
    reorder = db.collection('Reorder').where("vendor_ref","==",vendor).get()
    reorderlist=[]
    total_amount=0
    today = datetime.now()
    for r in reorder:
       a=r.to_dict()
       total_amount=total_amount+(a["purchase_price"]* a["reorderquantity"])
    purchase = db.collection('Purchase').add({'purchase_from_vendor_date':today,'total_amount':total_amount,
    'purchase_status':'Completed','vendor_purchase_ref':vendor,'recepiant':'BigShope','active':'true'})
    
    for r in reorder:
       a=r.to_dict()
       check = a["stock_ref"]
       if check == 0:
         sttt = db.collection('Stock').add({'quantity':a['reorderquantity'],'cost_price':a["purchase_price"],'purchase_date':today,'price':a["selling_price"],
        'pro_refer':a['product_ref'],'active':'true'})
         sttref = db.document('Stock/'+sttt[1].id)
         db.collection('Purchasedetails').add({'purchase_id':purchase[1].id,'selling_price':a["selling_price"],
        'cost_price':a["purchase_price"],'purchase_product':a['product_ref'],'purchase_stock':sttref,'quantity':a['reorderquantity'],'active':'true'})
         reorder = db.collection('Reorder').where("vendor_ref","==",vendor).get()
         for re in reorder:
            db.collection('Reorder').document(re.id).delete()       
         return redirect(vendorindex) 
       stocks =  a["stock_ref"].get()
       stock = stocks.to_dict()  
       if stock["purchase_date"] == a["reorder_date"]:
        stockid = stocks.id
        quantity=stock['quantity'] + a['reorderquantity']
        db.collection('Stock').document(stockid).update({'quantity':quantity,'cost_price':a["purchase_price"],'purchase_date':today,'active':'true'})
        db.collection('Purchasedetails').add({'purchase_id':purchase[1].id,'selling_price':a["selling_price"],
        'cost_price':a["purchase_price"],'purchase_product':a['product_ref'],'purchase_stock':a['stock_ref'],'quantity':a['reorderquantity'],'active':'true'})
        
        
              #purchase
              #puchasedetails
              #stockupdate
       else:
        db.collection('Stock').add({'quantity':a['reorderquantity'],'cost_price':a["purchase_price"],'purchase_date':today,'price':a["selling_price"],
        'pro_refer':a['product_ref'],'active':'true'})
        db.collection('Purchasedetails').add({'purchase_id':purchase[1].id,'selling_price':a["selling_price"],
        'purchase_price':a["purchase_price"],'purchase_product':a['product_ref'],'purchase_stock':a['stock_ref'],'quantity':a['reorderquantity'],'active':'true'})

         #purchase
              #puchasedetails
              #newstock
    reorder = db.collection('Reorder').where("vendor_ref","==",vendor).get()
    for re in reorder:
        db.collection('Reorder').document(re.id).delete()       
    return redirect(vendorindex) 

def reorderequest(request, productid):
    if request.session.is_empty():
        return redirect(logs) 
    pro_refer=db.document('Product/'+productid)
    reorderquantity = 1000
    date = datetime.today()
    pv = db.collection('Product').document(productid).get().to_dict()
    l = ["true","false"]
    stocks=db.collection('Stock').order_by('purchase_date',direction=firestore.Query.DESCENDING).limit(1).where("pro_refer","==",pro_refer).where('active','in',l).get()
    if stocks == []:
        stock_ref=0
        vprice=db.collection('Vendorstock').document(productid).get().to_dict()
        db.collection('Reorder').add({'reorder_status':'Not confirmed','vendor_ref':pv["vendor"],'product_ref':pro_refer,'stock_ref':stock_ref,'reorder_date':date,
        'reorderquantity':reorderquantity,'purchase_price':vprice['cprice'],'selling_price':vprice["sprice"]})
        messages.success(request,'Reorder request sent')
        return redirect(adminproduct)  
    for st in stocks:
        stock_ref=db.document('Stock/'+st.id)
        vprice=db.collection('Vendorstock').document(productid).get().to_dict()
        db.collection('Reorder').add({'reorder_status':'Not confirmed','vendor_ref':pv["vendor"],'product_ref':pro_refer,'stock_ref':stock_ref,'reorder_date':date,
        'reorderquantity':reorderquantity,'purchase_price':vprice['cprice'],'selling_price':vprice["sprice"]})
    messages.success(request,'Reorder request sent')
    return redirect(adminproduct)

def reorderequests(request):
    if request.session.is_empty():
        return redirect(logs) 
    reorder = db.collection('Reorder').where('reorder_status','==','Not confirmed').get()
    
    reorderlist = []
    total = 0
    for r in reorder:
        rid = r.id
        rd = r.to_dict()
        p = rd["product_ref"].get().to_dict()
        v = rd["vendor_ref"].get().to_dict()
        rd["rid"]=rid
        total = total + rd["purchase_price"]
        res = rd | v | p
        reorderlist.append(res)
    context = {'reorderlist':reorderlist,'total':total}    
    return render(request,'home/reorderequests.html',context)
def reorderconfirms(request):
    if request.session.is_empty():
        return redirect(logs) 
    reorder = db.collection('Reorder').where('reorder_status','==','Confirmed').get()
    
    reorderlist = []
    total = 0
    for r in reorder:
        rid = r.id
        rd = r.to_dict()
        p = rd["product_ref"].get().to_dict()
        v = rd["vendor_ref"].get().to_dict()
        rd["rid"]=rid
        total = total + rd["purchase_price"]
        res = rd | v | p
        reorderlist.append(res)
    context = {'reorderlist':reorderlist,'total':total}    
    return render(request,'home/reorderconfirms.html',context)    
def confirmreorders(request):
    reorder = db.collection('Reorder').where('reorder_status','==','Not confirmed').get()
    for r in reorder:
        db.collection('Reorder').document(r.id).update({'reorder_status':'Confirmed'})
    messages.success(request,"Reorders Confirmed")  
    return redirect(reorderequests)
def cancelreorder(request, reorderid):
    db.collection('Reorder').document(reorderid).delete()
    messages.success(request,"Canceled") 
    return redirect(reorderequests)
def cancelvendoreorder(request, reorderid):
    db.collection('Reorder').document(reorderid).delete()
    messages.success(request,"Canceled") 
    return redirect(vendor)    
def confirmsingle(request, reorderid):
    db.collection('Reorder').document(reorderid).update({'reorder_status':'Confirmed'})
    messages.success(request,"Reorders Confirmed") 
    return redirect(reorderequests)
def vendorstock(request):
    id=request.session["id"]
    vendor=db.document('Vendor/'+id)

    products = db.collection('Product').where('vendor','==',vendor).get()
    plist=[]
    for p in products:
        pd=p.to_dict()
        pd["pid"]=p.id
        plist.append(pd)
    v=[]
    vdet = db.collection('Vendorstock').where('vendor_ref','==',vendor).get()
    for vd in vdet:
        vdict = vd.to_dict()
        pd=vdict['vproduct'].get().to_dict()
        res = vdict | pd
        v.append(res)
    context = {'v':v,'products':plist}    
    return render(request,'vendor/vendorstock.html',context)

def vendoradd(request):
    if request.method=='POST':
        vproduct = request.POST['vproduct']
        vproducts={}
        context={}
        id = 0
        name=""
        vproducts = db.collection('Vendorstock').document(vproduct).get().to_dict()
        if vproducts == None:
            id = vproduct
            name=db.collection('Product').document(id).get()
        else:  
            vproducts['productid']=vproduct
            products = vproducts['vproduct'].get().to_dict()
            res = vproducts | products
        context={'vproducts':res,'id':id,'name':name} 
    return render(request,'vendor/vendoradd.html',context)
def addprices(request):
    if request.method=='POST':
        id=request.session["id"]
        vendor=db.document('Vendor/'+id)
        vproduct = request.POST['vproduct'] 
        product=db.document('Product/'+vproduct)
        cprice = request.POST['cprice']
        sprice = request.POST['sprice']
        process = request.POST['process']
        if process == 'add':
             db.collection('Vendorstock').document(vproduct).set({
            'vproduct':vendor,'product_ref':product,'cprice':cprice,'sprice':sprice,'active':'true'
             })

        if process == 'update':
            db.collection('Vendorstock').document(vproduct).update({
            'cprice':cprice,'sprice':sprice
             })
            a=db.collection('Reorder').where('product_ref','==',product).get()
            if a == []:
                return redirect(vendorstock)
            for i in a:
                db.collection('Reorder').document(i.id).update({'purchase_price':cprice,'selling_price':sprice})
    return redirect(vendorstock)         

def vendorupdate(request):  
    if request.method=='POST':
        vproduct = request.POST['vproduct']
        vc_price=request.POST['vc_price']
        vs_price = request.POST['vs_price']
        db.collection('Vendorstock').document(vproduct).update({'vc_price':vc_price,'vs_price':vs_price})
        return redirect(vendorstock)
    

def updatec(request,p,q):
    q=int(q)
    proref = db.document('Product/'+p)
    rs=db.collection('Reorder').where('product_ref','==',proref).get()
    for r in rs:
        db.collection('Reorder').document(r.id).update({'purchase_price':q})
    db.collection('Vendorstock').document(p).update({'cprice':q})    
    return redirect(vendor)
def updates(request,p,q):
    q=int(q)
    proref = db.document('Product/'+p)
    rs=db.collection('Reorder').where('product_ref','==',proref).get()
    for r in rs:
        db.collection('Reorder').document(r.id).update({'selling_price':q})
    db.collection('Vendorstock').document(p).update({'sprice':q})    
    return redirect(vendor)    
def updatecc(request,p,q):
    q=int(q)
    proref = db.document('Product/'+p)
    rs=db.collection('Reorder').where('product_ref','==',proref).get()
    for r in rs:
        db.collection('Reorder').document(r.id).update({'purchase_price':q})
    db.collection('Vendorstock').document(p).update({'cprice':q})    
    return redirect(vendorproduct)
def updatess(request,p,q):
    print("Ithano")
    q=int(q)
    proref = db.document('Product/'+p)
    rs=db.collection('Reorder').where('product_ref','==',proref).get()
    for r in rs:
        db.collection('Reorder').document(r.id).update({'selling_price':q})
    db.collection('Vendorstock').document(p).update({'sprice':q})    
    return redirect(vendorproduct)  
def quantityupdate(request,p,q):
    q=int(q)
    print(q)
    db.collection('Reorder').document(p).update({'reorderquantity':q})
    return redirect(vendor)
def quantityupdateadmin(request,p,q):
    q=int(q)
    db.collection('Reorder').document(p).update({'reorderquantity':q})
    return redirect(reorderequests)    
def payreport(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    return redirect('/corder')
def corder(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    return redirect('/order')         
def orders2(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    id=request.session['id']
    cusid=db.document("Customer/"+id)
    orders=db.collection('Orders').where("cus_order","==",cusid).where("order_status","==","completed").get()
    orderlist=[]
    for o in orders:
        odict=o.to_dict()
        odict["orderid"]=o.id
        orderlist.append(odict)   
    orderdetails=db.collection('Orderdetails').get()
    orderdetailslist=[]
    for od in orderdetails:
        odicts=od.to_dict()
        odicts["orderdetailsid"]=od.id
        orderid = odicts['orderid'].get().id
        odicts["order_id"]=orderid
        product = odicts['orderproduct'].get()
        productid = product.id 
        productdetails = product.to_dict()
        productdetails["productid"]=productid
        res = odicts | productdetails
        orderdetailslist.append(res)
 
    context = {'orders':orderlist,'orderdetails':orderdetailslist}
    return render(request,'ecom/orders.html',context)
# def order(request):
#     if request.session.is_empty():
#         return render(request,'ecom/page-login.html')
#     id=request.session['id']
#     orders=Orders.objects.filter(customer_id=id,status=1)
#     orderdetails=Orderdetails.objects.all()
#     products=Product.objects.all()
#     return render(request,'ecom/order.html',{'orders':orders,'orderdetails':orderdetails,'products':products}) 
def order2(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    id=request.session['id']
    cusid=db.document("Customer/"+id)
    orders=db.collection('Orders').order_by('orderdate',direction=firestore.Query.DESCENDING).where("cus_order","==",cusid).where("order_status","==","Ordered").get()
    orderlist=[]
    for o in orders:
        odict=o.to_dict()
        odict["orderid"]=o.id
        cus = odict["cus_order"].get().to_dict()
        loc= odict["loc_order"].get().to_dict()
        res = odict | cus | loc
        orderlist.append(res)   
    context = {'orders':orderlist}
    print(orderlist)
    return render(request,'ecom/allorders.html',context)
def allorderdetails(request,orderid):
    if request.session.is_empty():
        return redirect(logs)
    # orderref=db.collection('Orders').document(orderid).get().id
    orderref=db.document('Orders/'+ orderid)
    Orderdetails = db.collection('Orderdetails').where('orderid','==',orderref).get()
    currento=db.collection('Orders').document(orderid).get()
    current = currento.to_dict()
    locdict = current["loc_order"].get().to_dict()
    currentorder = locdict | current

    customer=currentorder["cus_order"].get().to_dict()
    result=[]
    for order in Orderdetails:
        orderdict=order.to_dict()
        productdict = orderdict["orderproduct"].get().to_dict()
        
        res = orderdict | productdict
        result.append(res)     
    context = {"orderdetails":result,"order":currentorder,"customer":customer}      
    return render(request,'ecom/allorderdetails.html',context)    
def cancelorder(request,id):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    # order=Orders.objects.get(order_id=id)
    # order.status=2
    # order.save()
    messages.success(request, ("Order Cancelled"))
    return redirect('/order')
def changepassword(request):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    id=request.session['id']
    # data = Customer.objects.get(id=id)
    return render(request,'ecom/changepassword.html')
def password(request,id):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    if request.method=='POST':
        password=request.POST['password1']
        # data = Customer.objects.get(id=id)
        # data.password= password
        # data.save()
        return redirect('/profile')  
def removeaccount(request):
    # if request.session.is_empty():
    #     return render(request,'ecom/page-login.html')
    # id = request.session['id']
    # data = Customer.objects.get(id=id)
    # data.active= 0
    # data.save()
    mail='aravindvinod709@gmail.com'
    email_from = settings.EMAIL_HOST_USER
    res = send_mail("hello me", "comment tu vas?", email_from, [mail])
    return redirect('/logs')

       
def what(request):
    # what = "hai"
    # if request.method=="POST":
    #     what = request.POST['what']
    #     try:
    #         datetime.strptime(what,'%Y-%m-%d')
    #         what = what
    #         a = Feedback.objects.create(date=what)
    #         a.save()
    #     except ValueError:
    #         what=None
    #         a = Feedback.objects.create(date=what)
    #         a.save()

    # count = Chumma.objects.all().count()
    # id = 1000
    # newid = id+count
    # chumma = Chumma.objects.create(id=newid)
    # chumma.save()
    # return render(request,"ecom/a.html")
    # return render(request,'ecom/a.html',{"what":what})
    # chumma = Chumma.objects.all()
   
    # for c in chumma:
    #     chumma2=Chumma.objects.exclude(userid_id=c.userid_id)

    # authe.update_user(disabled=True)    

    return render(request,'ecom/a.html')

def orderstatus(request, id):
    if request.session.is_empty():
        return render(request,'ecom/page-login.html')
    # orders = Orders.objects.get(order_id=id) 
    # orders.status="2"   
    # orders.status2="Delivered"
    # orders.save()
    return redirect('/shipper')

def report(request,id):
        if request.session.is_empty():
            return render(request,'ecom/page-login.html')
   
        payment="T389823298"
       

        order = db.collection('Orders').document(id).get().to_dict()
        location = order['loc_order'].get().to_dict()
        customer = order['cus_order'].get().to_dict()
        ordersid = db.document('Orders/'+id)
        orderdetails = db.collection('Orderdetails').where('orderid','==',ordersid).get()

        response = HttpResponse(content_type='application/pdf') 
        response['Content-Disposition']='attachment;filename="file.pdf"'
        p = canvas.Canvas(response)
        
        p.drawString(240,800,"Big Shope")
        p.drawString(300,780,"     ")
        p.drawString(230,760,"Purchase Receipt")
        p.drawString(300,750,"     ")
        p.drawString(100,720,"Or"+str(order['orderdate'])+str(id))  
      
        p.drawString(100,660,"Name:                               Transcation id                           Order date")
        p.drawString(100,640,".............................................................................................................")
        
        p.drawString(100,620,customer["customer_name"] + "                            "+payment+"                        "+str(order["orderdate"]))
        p.drawString(60,560,"Delivery address:     "+location['address'] + " "+ location['city'] + " "+ location['district']+", "+str(location['pin']))
        p.drawString(240,520,"Products : ")
        i=100
        j=460
        for odict in orderdetails:
            ors = odict.to_dict()
            producting = ors['orderproduct'].get().to_dict()
            p.drawString(i,j,producting['name']+" \n   Quantity :  " + str(ors['quantity'])+ " \n Unit Price : "+ str(ors['unitprice'])+" \n Subtotal : "+ str(ors['totalprice']))
            j=j-40


      
        p.drawString(180,j-40,"Inclusive of all taxes  Total Amount :    "+str(order['amount']))
        p.showPage()
        p.save()
        #messages.success(request, ("Order Successful")) 
        # feed = Feedback.objects.create(filepath="file.pdf")
        # feed.save()
        
        return FileResponse(response,content_type='application/pdf')











def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=models.Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'ecom/customer_home.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'ecom/index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})


#######################

def adminhome(request):
     return render(request,'home/profile2.html')
def adminicons(request):
    if request.session.is_empty():
        return redirect(logs) 
    products = db.collection('Product').get()
    product = []
    for p in products:
        pro = p.to_dict()
        pro["id"] = p.id
        product.append(pro)
    stocks = db.collection('Stock').get()
    stock = []
    for s in stocks:
        st = s.to_dict()
        st["id"] = s.id
        stock.append(st)
    context={
        'product':product,
        'stock':stock
    }    

    return render(request,'home/tables.html',context)     
def adminstock(request,product_id):
    if request.session.is_empty():
        return redirect(logs) 
    pro_refer = db.document('Product/'+product_id)    
    stocks = db.collection('Stock').where('pro_refer','==',pro_refer).get()
    stock = []
    total=0
    for s in stocks:
        st = s.to_dict()
        st["id"] = s.id
        prodetails = st["pro_refer"].get()
        prodict=prodetails.to_dict()
        st["name"] = prodict["name"]
        st["productimage"] = prodict["productimage"]
        stock.append(st)
    stockcount = db.collection('Stock').where('pro_refer','==',pro_refer).where('active','==','true').get()
    for count in stockcount:
        countdict = count.to_dict()
        total=total + int(countdict["quantity"])
    context={
        'stock':stock,
        'total':total
    }    
    return render(request,'home/adminstock.html',context)  

def adminproduct(request):
    if request.session.is_empty():
        return redirect(logs) 
    products = db.collection('Product').get()
    product = []
    pq=0
    for p in products:
        pro = p.to_dict()
        pro["id"] = p.id
        cat = pro["category"].get()
        a=cat.to_dict()
        pro["category"]=a["category_name"]
        # category = db.collection('persons').get()
        subcat = pro["subcategory"].get()
        b = subcat.to_dict()
        pro["subcategory"]=b["subcategory_name"]  
        v = pro['vendor'].get().to_dict()
        pro["vname"]=v["vname"]
        res = pro 
        print(res)
        print("/////////////////////////////////////////////////////////////////////////")
        prorefer = db.document('Product/'+p.id)
        pscheck = db.collection('Stock').where('pro_refer','==',prorefer).where('active','==','true').get()
        for ps in pscheck:
            psd = ps.to_dict()
            pq = pq + psd['quantity']
        res["totalstock"]  = pq
        pq=0
        product.append(res) 
    context={
        'product':product,
    }    
    return render(request,'home/adminproduct.html',context)

def editproduct(request,proid):
    if request.session.is_empty():
        return redirect(logs) 
    products = db.collection('Product').document(proid).get().to_dict()
    products["id"] = proid
    subcategory = products['subcategory'].get().to_dict()
    catdetails = products['category'].get().id
    products["cat_id"]=catdetails
    res =  products | subcategory

    category = db.collection('persons').get()
    subcats = []
    for cat in category:
      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)
    brands=db.collection('Brand').get()
    brandlist=[]
    for br in brands:
        bd = br.to_dict()
        bd["brandid"]=br.id
        brandlist.append(bd)       
    context={
        'product':res,
        'subcategory':subcats,
        'brandlist':brandlist
    }   
    return render(request,'vendor/editproduct.html',context)

def disableproduct(request,proid):
    if request.session.is_empty():
        return redirect(logs) 
    db.collection('Product').document(proid).update({'active':'false'})
    stock = db.collection('Stock').get()
    for s in stock:
        stocks = s.to_dict()
        pro = stocks['pro_refer'].get()
        if pro.id == proid:
             db.collection('Stock').document(s.id).update({'active':'false'})


    messages.success(request,"Disabled")
    return redirect('/adminproduct')

def enableproduct(request,proid):
    if request.session.is_empty():
        return redirect(logs) 
    db.collection('Product').document(proid).update({'active':'true'})
    stock = db.collection('Stock').get()
    for s in stock:
        stocks = s.to_dict()
        pro = stocks['pro_refer'].get()
        if pro.id == proid:
             db.collection('Stock').document(s.id).update({'active':'true'})


    messages.success(request,"Enabled")
    return redirect('/adminproduct')
    
def vdisableproduct(request,proid):
    if request.session.is_empty():
        return redirect(vlog) 
    db.collection('Product').document(proid).update({'active':'false'})
    stock = db.collection('Stock').get()
    for s in stock:
        stocks = s.to_dict()
        pro = stocks['pro_refer'].get()
        if pro.id == proid:
             db.collection('Stock').document(s.id).update({'active':'false'})


    messages.success(request,"Disabled")
    return redirect('/vendorproduct')

def venableproduct(request,proid):
    if request.session.is_empty():
        return redirect(logs) 
    db.collection('Product').document(proid).update({'active':'true'})
    stock = db.collection('Stock').get()
    for s in stock:
        stocks = s.to_dict()
        pro = stocks['pro_refer'].get()
        if pro.id == proid:
             db.collection('Stock').document(s.id).update({'active':'true'})


    messages.success(request,"Enabled")
    return redirect('/vendorproduct')    

def disablestock(request,sid):
    if request.session.is_empty():
        return redirect(logs) 
    products = db.collection('Stock').document(sid).update({'active':'disabled'})
    p= db.collection('Stock').document(sid).get().to_dict()
    proid=p["pro_refer"].get().id
    messages.success(request,"Disabled")
    return redirect(adminstock, product_id=proid)  

def enablestock(request,sid):
    if request.session.is_empty():
        return redirect(logs)
    products = db.collection('Stock').document(sid).update({'active':'true'})
    p= db.collection('Stock').document(sid).get().to_dict()
    proid=p["pro_refer"].get().id
    messages.success(request,"Enabled")
    return redirect(adminstock, product_id=proid)           


def updateproduct(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        proid=request.POST.get('productid')
        name = request.POST.get('name')
        today = datetime.now()
        category= request.POST['category']
        print(category)
        if category =='other':
            cat= request.POST.get('catadd')
            sub= request.POST.get('subadd')
            a=db.collection('persons').where('category_name','==',cat).get()
            if a==[]:
                cats = db.collection('persons').add({'name':cat,'category_name':cat,'active':'true','category_date':today})
                
                subcats = db.collection('persons').document(cats[1].id).collection('subcategory').add({'subcategory_name':sub,'active':'true','subcategory_date':today})
                print(subcats[1].id)
                print(cats[1].id)
                sub_ref=db.document('persons/'+cats[1].id+'/subcategory/'+subcats[1].id)
                cat_ref=db.document('persons/'+cats[1].id)
            else:
                for i in a:
                   cat_ref=db.document('persons/'+i.id)
                   subcats = db.collection('persons').document(i.id).collection('subcategory').add({'subcategory_name':sub})
                   sub_ref=db.document('persons/'+i.id+'/subcategory/'+subcats[1].id)
        else:    
            category = category.split(",")
            sub_ref=db.document('persons/'+category[1]+'/subcategory/'+category[0])
            cat_ref=db.document('persons/'+category[1])
        desc = request.POST.get('desc')
        brand = request.POST.get('brand')
        if brand =='other':
            bradd= request.POST.get('bradd')
            b=db.collection('Brand').where('brandname','==',bradd).get()
            if b==[]:
                brads = db.collection('Brand').add({'brandname':bradd,'branddate':today,'active':'true'})
                brandref = bradd
            else:  
                brandref = bradd
        else:
            brandref = brand
        details = request.POST.get('details')
        db.collection('Product').document(proid).update({'name':name,'description':desc,'details':details,'brand':brandref,'active':'true','category':cat_ref,'subcategory':sub_ref,'sub':sub_ref.get().id})
        messages.success(request,"Succsessfully Updated")
        return redirect('/vendorproduct')  
def adminbrand(request):
    cats=db.collection('persons').get()
    catlist=[]
    for cat in cats:
        cd = cat.to_dict()
        cd["catid"]=cat.id
        catlist.append(cd)
    print(catlist)    
    context={'catlist':catlist}    
    return render(request,'home/addbrand.html',context)
def addbrand(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        brandname = request.POST['brandname'] 
        today=datetime.now()
        db.collection('Brand').add({'brandname':brandname,'branddate':today,'active':'true'})    
    return redirect(adminbrand)
def addcategory(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        cname = request.POST['categoryname'] 
        today=datetime.now()
        db.collection('persons').add({'category_name':cname,'name':cname,'category_date':today,'active':'true'})    
    return redirect(adminbrand)       
def addsubcategory(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        cid = request.POST['categoryid'] 
        sname = request.POST['subcategoryname'] 
        today=datetime.now()
        db.collection('persons').document(cid).collection('subcategory').add({'subcategory_name':sname,'subcategory_date':today,'active':'true'})    
    return redirect(adminbrand)           
# def stockadd(request):
#     product_id = "watch"
#     product=db.collection('Product').document(product_id).get().to_dict()
#     pro_refer = db.document('Product/')
#     cost_price=500
#     price=1000
#     quantity = 20
#     p=product["name"]
#     stock=db.collection('Stock').add({'pro_refer':pro_refer,'cost_price':cost_price,'price':price,'quantity':20})
#     stock[1].id   
#     for i in range(1, quantity):
#         stock=db.collection('Stock').document(stock[1].id).collection('Item').add({'itemid':stock[1].id+product["name"]+i,'stockid':stock[1].id})

#     return redirect(viewsales)
def insertions(request):
    a="Minty"
    b=datetime.now()
    bb="4nEdDmw8CD8KXSUNTdff"
    bbb="2ZBtQ2Ej59eZpcYGE7Go"
    cc_ref=db.document('persons/'+bb+'/subcategory/'+bbb)
    aa=cc_ref.get()
    print(aa.to_dict())
    #db.collection('Product').add({'name':a,'added_date':b,'ref':cc_ref})
    #db.collection('Product').document('iphone').update({'name':'iphone'})
    return render(request,'ecom/a.html')
def productadd(request):
    if request.session.is_empty():
        return redirect(logs)
    category = db.collection('persons').get()
    subcats = []
    for cat in category:
      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)
    brands=db.collection('Brand').get()
    brandlist=[]
    for br in brands:
        bd = br.to_dict()
        bd["brandid"]=br.id
        brandlist.append(bd) 
    vendor=db.collection('Vendor').where('active','==','true').get()
    vendorlist=[]
    for v in vendor:
        vd = v.to_dict()
        vd["vendorid"]=v.id
        vendorlist.append(vd)       
    context={'subcategory':subcats,'brandlist':brandlist,'vendorlist':vendorlist}

    return render(request,'home/addproduct.html',context)     

def addproduct(request):
    if request.session.is_empty():
        return redirect(logs)
    if request.method=='POST':
        name = request.POST['name']
        category= request.POST['category']
        category = category.split(",")
        sub_ref=db.document('persons/'+category[1]+'/subcategory/'+category[0])
        cat_ref=db.document('persons/'+category[1])
        desc = request.POST['desc']
        brand = request.POST['brand']
        vendor = request.POST['vendor']
        vendor_ref = db.document('Vendor/'+vendor)
        details = request.POST['details']
        added_date=datetime.now()

        image = request.FILES['image']
        # fs = FileSystemStorage(location='.static\product_image') #defaults to   MEDIA_ROOT  
        fs = FileSystemStorage(location='./static/product_image')
        filename = fs.save(image.name,image)
        file_url = fs.url(filename)
        product_image='product_image'+file_url+''
        
        newproduct=db.collection('Product').add({'name':name,'added_date':added_date,'description':desc,'details':details,'brand':brand,'active':'true','category':cat_ref,'subcategory':sub_ref,'productimage':product_image,'sub':category[0],'vendor':vendor_ref,'reorder':'active'})
        newp_ref = db.document('Product/'+newproduct[1].id)
        db.collection('Vendorstock').document(newproduct[1].id).set({
            'vproduct':newp_ref,
            'vendor_ref':vendor_ref,
            'cprice':0,
            'sprice':0,
            'active':'true'
        })
        messages.success(request,"Succsess")
        return redirect('/productadd')
    return render(request,'home/addproduct.html')   


def adminorders(request):
    if request.session.is_empty():
        return redirect(logs)
    Orders = db.collection('Orders').order_by('orderdate',direction=firestore.Query.DESCENDING).get()
    order=[]
    for o in Orders:
        odict = o.to_dict()
        odict["order_id"]=o.id
        cusdict = odict["cus_order"].get().to_dict()
        locdict = odict["loc_order"].get().to_dict()
        res=odict | cusdict | locdict
        order.append(res)
    context={
        'order':order
    }    
    return render(request,'home/adminorder.html',context)  

def adminorderdetails(request,orderid):
    if request.session.is_empty():
        return redirect(logs)
    # orderref=db.collection('Orders').document(orderid).get().id
    orderref=db.document('Orders/'+ orderid)
    Orderdetails = db.collection('Orderdetails').where('orderid','==',orderref).get()
    currento=db.collection('Orders').document(orderid).get()
    current = currento.to_dict()
    locdict = current["loc_order"].get().to_dict()
    currentorder = locdict | current

    customer=currentorder["cus_order"].get().to_dict()
    result=[]
    for order in Orderdetails:
        orderdict=order.to_dict()
        productdict = orderdict["orderproduct"].get().to_dict()
        
        res = orderdict | productdict
        result.append(res)     
    context = {"orderdetails":result,"order":currentorder,"customer":customer}      
    return render(request,'home/adminorderdetails.html',context) 

# def sales(request):
#     if request.session.is_empty():
#         return redirect(logs)
#     order=[]
#     d=datetime.now()
#     only_date, only_time = d.date(), d.time()
    
#     s = db.collection('Orders').get()
#     for sal in s:
#         sale=sal.to_dict()
#         dd = sale["orderdate"]
#         only_date=dd.date()
        
#         if dd.date().month == d.date().month:
#             print(sale["order_status"])
#             print(sal.id)
#             sale["order_id"] = sal.id
#             cusdict = sale["cus_order"].get().to_dict()
#             res=sale | cusdict
#             order.append(res)
#     context={
#                 'order':order
#     }    
#     return render(request,'home/adminorder.html',context)  


def admincustomer(request):
    if request.session.is_empty():
        return redirect(logs)
    customers = db.collection('Customer').get()
    customer=[]
    for c in customers:
        cdict=c.to_dict()
        customer.append(cdict)
    context={'customer':customer}    
    return render(request,'home/admincustomer.html',context)  


def adminlogout(request):
    if request.session.is_empty():
        return redirect(adminlogs)
    authe.current_user=None    
    request.session.flush()
    return redirect('/adminlogs')    

def logout(request):
    if request.session.is_empty():
        return redirect(logs)  
    authe.current_user=None
    request.session.flush()
    return redirect(logs) 
def vlogout(request):
    if request.session.is_empty():
        return redirect(logs3)  
    authe.current_user=None
    request.session.flush()
    return redirect(logs3)     

def editpage(request):
    return render(request, "home/editimages.html")   
def editimages(request):
    if request.method=='POST':
        image=request.FILES['image']
    
       
        bucket = storage.bucket()
        blob = bucket.blob(image.name)
        blob.upload_from_file(
                image,
                content_type='image/jpeg'
            )
        blob.make_public()    
        print(blob.public_url)

        return redirect(adminproduct)

# client=storage.Client()
# bucket = client.get_bucket('e-commerce-a39dc.appspot.com')  
def adminvendor(request):
    vendor=db.collection('Vendor').where('active','==','true').get()
    vendorlist=[]
    for v in vendor:
        vd = v.to_dict()
        vd["vendorid"]=v.id
        vendorlist.append(vd)       
    context={'vendorlist':vendorlist}
    return render(request,'home/adminvendor.html',context)
def viewsales(request):
    if request.session.is_empty():
        return redirect(logs)
    return render(request,'home/adminsales.html')      
def sales(request):
    if request.session.is_empty():
        return redirect(logs)
      
    order=[]
    d=datetime.now()
    only_date, only_time = d.date(), d.time()
    
    s = db.collection('Orders').get()
    for sal in s:
        sale=sal.to_dict()
        dd = sale["orderdate"]
        only_date=dd.date()
        
        if dd.date().month == d.date().month:
            print(sale["order_status"])
            print(sal.id)
            sale["order_id"] = sal.id
            cusdict = sale["cus_order"].get().to_dict()
            res=sale | cusdict
            order.append(res)
    context={
                'order':order
    }    
    return render(request,'home/adminorder.html',context)
def disablereorder(request,pid):
    db.collection('Product').document(pid).update({'reorder':'disabled'})
    return redirect(adminproduct) 
def enablereorder(request,pid):
    db.collection('Product').document(pid).update({'reorder':'active'})
    return redirect(adminproduct)        
def monthsales(request,month):
    if request.session.is_empty():
        return redirect(logs)
      
    order=[]
    monthdetails={}
    product=[]
    productdict={}
    count =0
    no_of_products=0
    cost_price = 0
    money=0
    eachproductquantity=0
    overallcostamount=0
    
    if month == 0:
         d=datetime.now()
         only_date, only_time = d.date(), d.time()
         month = only_date.month
    
    s = db.collection('Orders').get()
   
    for sal in s:
        totalcm=0
        sale=sal.to_dict()
        dd = sale["orderdate"]
        only_date=dd.date()
        
        if dd.date().month == month:
            # print(sale["order_status"])
            # print(sal.id)
            sale["order_id"] = sal.id
            orid = db.document('Orders/'+sal.id)
            ords = db.collection('Orderdetails').where("orderid","==",orid).get()
            for ord in ords:
                a=ord.to_dict()
                count = count + 1
                money = money + a["totalprice"]
                no_of_products = no_of_products + a["quantity"]
                stockdetails = a["orderstock"].get().to_dict()
                totalcosts = stockdetails["cost_price"] * a["quantity"]
                cost_price = cost_price + totalcosts

            monthdetails["ordercount"]=count
            monthdetails["money"]=money
            monthdetails["no_of_products"]=no_of_products
            monthdetails["cost_price"]=cost_price
            monthdetails["totalprofit"]= monthdetails["money"]-monthdetails["cost_price"]
            
           
            new_date = str(dd.date().month)+'-' + str(dd.date().year)
            format = '%m-%Y' # The format
            datetime_str = datetime.strptime(new_date, format)
            monthdetails["date"]=datetime_str.date()

            cusdict = sale["cus_order"].get().to_dict()
            locdict = sale["loc_order"].get().to_dict()

            #totalcostprice = 0
            for orcost in ords:
                orcostdict = orcost.to_dict()
               
                orcostd = orcostdict["orderstock"].get().to_dict()
                
                totalcostamount = orcostd["cost_price"] * orcostdict["quantity"]      
                print(orcostd["cost_price"])     
               
                totalcm = totalcm + totalcostamount

            totalsellamount=sale["amount"]
            print("total",totalcm)
            profititem =  totalsellamount - totalcm
            
            overallcostamount=overallcostamount +totalcm
            sale["totalcostamount"]= totalcm
            sale["totalsellamount"]=  totalsellamount
            sale["profititem"]= profititem
            monthdetails["overallcostamount"]=overallcostamount
            res=sale | cusdict | locdict
            order.append(res)

           
    context={
                'order':order,
                'monthdetails':monthdetails,
                'product':product
    }    
    return render(request,'home/adminsales.html',context) 
def monthproducts(request):
    return redirect(monthsales)

def rating(request):
    
    if request.method=='POST':
        login = request.session['id']
        customerid = db.document('Customer/'+login)
        prod = request.POST['productid']
        productid = db.document('Product/'+prod)
        stock = request.POST['stockid']
        stockid = db.document('Stock/'+stock)
        rating = request.POST['rating']
        review = request.POST['review']
        ratingid = request.POST['ratingid']
        print(ratingid)
        process = request.POST['process']
        print(process)
        if process == "add":
            db.collection('Rating').add({
            'cus_rating':customerid,
            'pro_rating':productid,
            'stock_rating':stockid,
            'rating':rating,
            'review':review
        })
        else:
             db.collection('Rating').document(ratingid).update({
            'cus_rating':customerid,
            'pro_rating':productid,
            'stock_rating':stockid,
            'rating':rating,
            'review':review})  

    messages.success(request,"Rating and Review added") 
    return redirect(single2, pid = prod, sid = stock)               
def ordereport(request,orderid):
    customerid = request.session["id"] 
    orderref = db.document("Orders/"+orderid)
    ordering = db.collection('Orders').document(orderid).get().to_dict()
    orderdetail=[]
    
    loc = ordering['loc_order'].get().to_dict()
    order = ordering | loc
    customering = db.collection('Customer').document(customerid).get().to_dict()
    orderdetails = db.collection('Orderdetails').where('orderid','==',orderref).get()
    for ordict in orderdetails:
            ors = ordict.to_dict()
            producting = ors["orderproduct"].get().to_dict()
            res = ors | producting
            orderdetail.append(res)

    context = {
       'order':order,
       'orderdetails':orderdetail,
       'customer':customering
    }   
    email_from = settings.EMAIL_HOST_USER
    res = send_mail("Big Shope Vendor Registartion, Use This Password to Sign in :{current} ",str(order), email_from, ['aravindvv2022a@mca.ajce.in'])
            # generate_random = int(generate_random)
    return render(request,'ecom/ordereport.html',context)        


def homepage(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'ecom/index2.html', context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        print("1")
        try:
            print("2")
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            print(payment_id)
            print(razorpay_order_id)
            print(signature)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            a=redirect(pay2)    
            a.set_cookie('razorpay_order_id', razorpay_order_id)
            a.set_cookie('razorpay_payment_id', payment_id)  
            if result is None:
                amount = 20000  # Rs. 200
                try:
                    print("3")
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return redirect(pay2)
                except:
 
                    # if there is an error while capturing payment.
                    return redirect(pay2)
            else:
 
                # if signature verification fails.
                return a

        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()



def vendorpurchase(request):
    id = request.session['id']
    pref = db.document('Vendor/'+id)
    purchases = db.collection('Purchase').order_by('purchase_from_vendor_date',direction=firestore.Query.DESCENDING).where('vendor_purchase_ref','==',pref).get()
    purchaselist=[]
    for p in purchases:
        pd = p.to_dict()
        pd["pid"]=p.id
        purchaselist.append(pd)
    print(purchaselist)    
    context={'purchaselist':purchaselist}
    return render(request,'vendor/vendorpurchase.html',context)
def adminpurchase(request):
    purchases = db.collection('Purchase').order_by('purchase_from_vendor_date',direction=firestore.Query.DESCENDING).get()
    purchaselist=[]
    for p in purchases:
        pd = p.to_dict()
        pd["pid"]=p.id
        vends = pd["vendor_purchase_ref"].get().to_dict()
        pd["vendorname"] = vends["vname"]
        purchaselist.append(pd)
    print(purchaselist)    
    context={'purchaselist':purchaselist}
    return render(request,'home/adminpurchase.html',context)
def vpurchasedetails(request, pid):    
    
    purchasedetails = db.collection('Purchasedetails').where('purchase_id','==',pid).get()
    purchaselist=[]
    for p in purchasedetails:
        pd = p.to_dict()
        pd["pdid"]=p.id
        ppro = pd["purchase_product"].get().to_dict()
        res = ppro | pd
        purchaselist.append(res)
    print(purchaselist) 
    purchase=  db.collection('Purchase').document(pid).get().to_dict()  
    purchase["pid"]=pid
    context={'purchaselist':purchaselist,'purchase':purchase}
    return render(request,'vendor/vendorpurchasedetails.html',context)
def adminpurchasedetails(request, pid):    
    
    purchasedetails = db.collection('Purchasedetails').where('purchase_id','==',pid).get()
    purchaselist=[]
    for p in purchasedetails:
        pd = p.to_dict()
        pd["pdid"]=p.id
        ppro = pd["purchase_product"].get().to_dict()
        res = ppro | pd
        purchaselist.append(res)
    print(purchaselist) 
    purchase=  db.collection('Purchase').document(pid).get().to_dict()  
    purchase["pid"]=pid
    context={'purchaselist':purchaselist,'purchase':purchase}
    return render(request,'home/adminpurchasedetails.html',context)   

def vaddproduct(request):
    if request.session.is_empty():
        return redirect(logs3)
    today = datetime.now()
    category = db.collection('persons').get()
    subcats = []
    for cat in category:
      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)
    brands=db.collection('Brand').get()
    brandlist=[]
    for br in brands:
        bd = br.to_dict()
        bd["brandid"]=br.id
        brandlist.append(bd) 
    vendor=db.collection('Vendor').where('active','==','true').get()
    vendorlist=[]
    for v in vendor:
        vd = v.to_dict()
        vd["vendorid"]=v.id
        vendorlist.append(vd)       
    context={'subcategory':subcats,'brandlist':brandlist,'vendorlist':vendorlist}

    return render(request,'vendor/vaddproduct.html',context) 

def vaddp(request):
    if request.session.is_empty():
        return redirect(logs3)
    vid = request.session["id"]  
    today = datetime.now()  
    if request.method=='POST':
        name = request.POST['name']
        category= request.POST['category']
        if category =='other':
            cat= request.POST.get('catadd')
            sub= request.POST.get('subadd')
            a=db.collection('persons').where('category_name','==',cat).get()
            if a==[]:
                cats = db.collection('persons').add({'name':cat,'category_name':cat,'active':'true','category_date':today})
                
                subcats = db.collection('persons').document(cats[1].id).collection('subcategory').add({'subcategory_name':sub,'active':'true','subcategory_date':today})
                print(subcats[1].id)
                print(cats[1].id)
                sub_ref=db.document('persons/'+cats[1].id+'/subcategory/'+subcats[1].id)
                cat_ref=db.document('persons/'+cats[1].id)
            else:
                for i in a:
                   cat_ref=db.document('persons/'+i.id)
                   subcats = db.collection('persons').document(i.id).collection('subcategory').add({'subcategory_name':sub})
                   sub_ref=db.document('persons/'+i.id+'/subcategory/'+subcats[1].id)


        else:    
            category = category.split(",")
            sub_ref=db.document('persons/'+category[1]+'/subcategory/'+category[0])
            cat_ref=db.document('persons/'+category[1])

        desc = request.POST['desc']
        brand = request.POST.get('brand')
        if brand =='other':
            bradd= request.POST.get('bradd')
            b=db.collection('Brand').where('brandname','==',bradd).get()
            if b==[]:
                brads = db.collection('Brand').add({'brandname':bradd,'branddate':today,'active':'true'})
                brandref = bradd
            else:  
                brandref = bradd
        else:
            brandref = brand
        vendor_ref = db.document('Vendor/'+vid)
        cprice = request.POST['cprice']
        sprice = request.POST['sprice']
        cprice = int(cprice)
        sprice=int(sprice)
        details = request.POST['details']
        added_date=datetime.now()

        image = request.FILES.get('image')
        product_image=0
        if image != None:
        # fs = FileSystemStorage(location='.static\product_image') #defaults to   MEDIA_ROOT  
            fs = FileSystemStorage(location='./static/product_image')
            filename = fs.save(image.name,image)
            file_url = fs.url(filename)
            product_image='product_image'+file_url+''
        
        newproduct=db.collection('Product').add({'name':name,'added_date':added_date,'description':desc,'details':details,'brand':brandref,'active':'true','category':cat_ref,'subcategory':sub_ref,'productimage':product_image,'sub':sub_ref.get().id,'vendor':vendor_ref,'reorder':'active'})
        newp_ref = db.document('Product/'+newproduct[1].id)
        db.collection('Vendorstock').document(newproduct[1].id).set({
            'vproduct':newp_ref,
            'vendor_ref':vendor_ref,
            'cprice':cprice,
            'sprice':sprice,
            'active':'true'
        })
        
        messages.success(request,"Succsess")
        return redirect('/vaddproduct')
    return render(request,'home/vaddproduct.html') 
def vendorproduct(request):
    if request.session.is_empty():
        return redirect(logs3) 
    vid = request.session["id"]    
    vendor_ref = db.document('Vendor/'+vid)     
    products = db.collection('Product').where('vendor','==',vendor_ref).get()
    product = []
    for p in products:
        pro = p.to_dict()
        pro["productid"] = p.id
        cat = pro["category"].get()
        a=cat.to_dict()
        pro["category"]=a["category_name"]
        # category = db.collection('persons').get()
        subcat = pro["subcategory"].get()
        b = subcat.to_dict()
        pro["subcategory"]=b["subcategory_name"]  
        v = db.collection('Vendorstock').document(p.id).get().to_dict()
        res = pro 
        res["cprice"]=v["cprice"]
        res["sprice"]=v["sprice"]
        product.append(res) 
    context={
        'product':product,
    }    
    return render(request,'vendor/vendorproduct.html',context)

def vendorbrand(request):
    cats=db.collection('persons').get()
    catlist=[]
    for cat in cats:
        cd = cat.to_dict()
        cd["catid"]=cat.id
        catlist.append(cd)
    print(catlist)    
    context={'catlist':catlist}    
    return render(request,'vendor/vendorbrand.html',context)
def addbrand(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        brandname = request.POST['brandname'] 
        today=datetime.now()
        db.collection('Brand').add({'brandname':brandname,'branddate':today,'active':'true'})    
    return redirect(vendorbrand)
def addcategory(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        cname = request.POST['categoryname'] 
        today=datetime.now()
        db.collection('persons').add({'category_name':cname,'name':cname,'category_date':today,'active':'true'})    
    return redirect(vendorbrand)       
def addsubcategory(request):
    if request.session.is_empty():
        return redirect(logs) 
    if request.method=='POST':
        cid = request.POST['categoryid'] 
        sname = request.POST['subcategoryname'] 
        today=datetime.now()
        db.collection('persons').document(cid).collection('subcategory').add({'subcategory_name':sname,'subcategory_date':today,'active':'true'})    
    return redirect(vendorbrand)   
def adminlocations(request):
    loc = db.collection('Pin').get()
    list=[]
    for l in loc:
        ld = l.to_dict()
        ld["pinid"]=l.id
        list.append(ld)
    context = {'list':list}    
    return render(request,'home/adminlocations.html',context)
def adminaddlocations(request): 
    return render(request,'home/adminaddlocations.html')                 
def disablepin(request,pinid):
    db.collection('Pin').document(pinid).update({'active':'false'})
    return redirect(adminlocations)
def enablepin(request,pinid):
    db.collection('Pin').document(pinid).update({'active':'true'})
    return redirect(adminlocations)   
def adminpinset(request): 
    if request.method=='POST':
        postoffice = request.POST.get('post_office')
        district = request.POST.get('district')
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        pin=int(pin)
        a=db.collection('Pin').document(pin).get().to_dict()
        print(a)
        if a == None:
            b= db.collection('Pin').document(pin).set({
            'post_office':postoffice,
            'city':city,
            'pin':pin,
            'district':district,
            'active':'true'
                                            })
        else:
           messages.error(request,"Pin already added") 
           return redirect(adminaddlocations)  

    return redirect(adminaddlocations)   

def addwish(request, pid, sid):
    cid = request.session['id']
    cref = db.document('Customer/'+cid)
    pref = db.document('Product/'+pid)
    today = datetime.today()
    db.collection('Wishlist').add({
        'cref':cref,
        'pref':pref,
        'active':'true',
        'wishdate':today
    })
    messages.success(request,"Added to your wishlist")
    return redirect(single2,pid=pid,sid=sid)

def removewish(request, pid, sid):
    cid = request.session['id']
    cref = db.document('Customer/'+cid)
    pref = db.document('Product/'+pid)
    wish=db.collection('Wishlist').where('cref','==',cref).where('pref','==',pref).get()
    for w in wish:
        db.collection('Wishlist').document(w.id).delete()
        messages.success(request,"Removed From Wishlist")
    if sid == 0:
        return redirect(wishlist)
    else:
        return redirect(single2,pid=pid,sid=sid)        
    
def wishlist(request):
    cid = request.session['id']
    cref = db.document('Customer/'+cid)
    wishlist=[]
    wish=db.collection('Wishlist').where('cref','==',cref).get()
    for w in wish:
        wd = w.to_dict()
        wd["wishid"]=w.id
        pref = wd["pref"].get().id
        stock=db.collection('Stock').where('pro_refer','==',wd["pref"]).where('active','==','true').get()
        for s in stock:
            sd = s.to_dict()
            print(sd)
            sd["pid"]=pref
            sd["sid"]=s.id
            product = sd["pro_refer"].get().to_dict()
            res = sd | product | wd
            wishlist.append(res)
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)         
    context = {'wishlist':wishlist,'cats':cats,'subcats':subcats}  
    
    return render(request,'ecom/wishlist.html',context)    











###########RECOMENDATION#############################################################


def recommendation(request):
    import pandas as pd
    row = []
    prolist=[]
    ratings=db.collection('Rating').get()
    for r in ratings:
        rd = r.to_dict()
        row.append([str(rd["cus_rating"].get().id),str(rd["pro_rating"].get().id),rd["rating"]])   
    products = db.collection('Product').get()
    for p in products:
        pms = p.to_dict()
        prolist.append([str(p.id),str(pms["name"])])
   
    rating = pd.DataFrame(row,columns=['userId','productId','rating'])
    product = pd.DataFrame(prolist,columns=['productId','title'])
   
    ratings2 = pd.merge(rating, product, how='inner', on='productId')
    df = ratings2.pivot_table(index='productId',columns='userId',values='rating').fillna(0)
    user=request.session["id"]
    num_neighbors=1
    num_recommendation=1

    prolists = product_recommender(user, num_neighbors, num_recommendation,df)
    category = db.collection('persons').get()
    cats = []
    subcats = []
   
    for cat in category:
      catdict = cat.to_dict()
      catdict["id"]=cat.id
      cats.append(catdict)

      subcat =  db.collection('persons').document(cat.id).collection('subcategory').get()
      for sub in subcat:
          subdict = sub.to_dict()
          subdict["sub_id"]=sub.id
          subdict["cat_id"]=cat.id
          subcats.append(subdict)
    context = {'wishlist':prolists,'cats':cats,'subcats':subcats}
    return render(request,'ecom/recoms.html',context)

def product_recommender(user, num_neighbors, num_recommendation,df):

  from sklearn.neighbors import NearestNeighbors 
  df1 = df.copy()
  number_neighbors = num_neighbors

  knn = NearestNeighbors(metric='cosine', algorithm='brute')
  knn.fit(df.values)
  distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)
  
  user_index = df.columns.tolist().index(user)
  for m,t in list(enumerate(df.index)):
    if df.iloc[m, user_index] == 0:
      
      sim_products = indices[m].tolist()
      
     
      product_distances = distances[m].tolist()
      # j = 1
      # print("Product Distances : ")
      # for i in sim_products:
          
      #     print(str(j)+': '+str(df.index[i])+', the distance with '+str(t)+': '+str(product_distances[j-1]))
      #     j = j + 1
      if m in sim_products:
        id_product = sim_products.index(m)
       
        sim_products.remove(m)
        
        product_distances.pop(id_product) 


      else:
        sim_products = sim_products[:num_neighbors-1]
        
        product_distances = product_distances[:num_neighbors-1]
           
      product_similarity = [1-x for x in product_distances]
      product_similarity_copy = product_similarity.copy()
      nominator = 0

      for s in range(0, len(product_similarity)):
        if df.iloc[sim_products[s], user_index] == 0:
          if len(product_similarity_copy) == (number_neighbors - 1):
            product_similarity_copy.pop(s)
          
          else:
            product_similarity_copy.pop(s-(len(product_similarity)-len(product_similarity_copy)))
            
        else:
         
          nominator = nominator + product_similarity[s]*df.iloc[sim_products[s],user_index]
          
      if len(product_similarity_copy) > 0:
        if sum(product_similarity_copy) > 0:
          predicted_r = nominator/sum(product_similarity_copy)
        
        else:
          predicted_r = 0

      else:
        predicted_r = 0
        
      df1.iloc[m,user_index] = predicted_r
      
      
  
  prolists = recommend_products(user,num_recommendation,df,df1) 
  return prolists   

def recommend_products(user, num_recommended_products,df,df1):

  print('The list of the Products {} user Bought \n'.format(user))

  for m in df[df[user] > 0][user].index.tolist():
    
    print(m)
  
  print('\n')

  recommended_products = []
  for m in df[df[user] == 0].index.tolist():

    index_df = df.index.tolist().index(m)
    predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
    
    recommended_products.append((m, predicted_rating))

  sorted_rm = sorted(recommended_products, key=lambda x:x[1], reverse=True)
  
  print('The list of the Recommended Products \n')
  rank = 1
  productlist=[]
  for recommended_product in sorted_rm[:num_recommended_products]:
    
    print('{}: {} -              predicted rating:{}'.format(rank, recommended_product[0], recommended_product[1]))
    #print('{}: {} '.format(rank, recommended_product[0]))
    productlist.append(recommended_product[0])
    rank = rank + 1
  prolists=[]  
  for p in productlist:

    pro_refer = db.document('Product/'+p)
    stock = db.collection('Stock').where('pro_refer','==',pro_refer).where('active','==','true').get()
    for s in stock:
        sd = s.to_dict()
        sd["sid"]=s.id
        sd["pid"]=p
        pd = sd["pro_refer"].get().to_dict()
        res = sd | pd
        prolists.append(res)
  return prolists
 

  
def vendorprofile(request):
    return render(request,'vendor/vendorprofile.html')
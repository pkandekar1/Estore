from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from ecommapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.
def home(request):
    context ={}
    context['name']="peter"
    context['age']=10
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':'20000'},
        {'id':2,'name':'jeans','cat':'cloth','price':'600'},
        {'id':3,'name':'addidas','cat':'shoes','price':'4000'},
        {'id':4,'name':'boat','cat':'earphone','price':'2000'},
        ]
    # return HttpResponse("This is home page")
    return render(request,'hello.html',context)
def home2(request):
    # userid=request.user.id
    # print("id of logged user",userid)
    context={}
    p=Product.objects.filter(is_activate=True)
    print(p)
    context['products']=p
    return render(request,'index.html',context)

def home3(request):
    context={}
    p=Product.objects.all()
    context['products']=p
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_activate=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    print(min)
    print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_activate=True)
    p=Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)
    return HttpResponse("value fetched")

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    p=Product.objects.filter(is_activate=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        # print("user is logged")
        u=User.objects.filter(id=request.user.id)
        # print(u)
        p=Product.objects.filter(id=pid)
        # print(p)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        n=len(c)
        context={}
        context['products']=p
        if n==1:
            context['msg']="product already exits"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product added successfully on cart"
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')

def dummyregistration(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST or None)
        if form.is_vaild():
            form.save()

    return render(request,'dummyregistration.html',{'form': form})

def registration(request):
    context={}
    if request.method == 'POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'registration.html',context)
        elif upass!=ucpass:
            context['errmsg']= "password and confirm password didn't match"
            return render(request,'registration.html',context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="user created successfully"
                return render(request,'registration.html',context)
            except Exception:
                context['errmsg']="user already exits"
                return render(request,'registration.html',context)
            # return HttpResponse("User created successfully")
    else:
        return render(request,'registration.html')
  
    # return render(request,'registration.html')
    

def login_user(request):
    context={}
    if request.method == 'POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            # print(u)
            # print(u.uemail)
            # print(u.is_superuser)
            # return HttpResponse("Authenticated")
            if u is not None:
                login(request,u) #start session and store id of logged in user session
                return redirect('/home2')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/home2')

def product_detail(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'product_details.html',context)

def place_order(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print("order_id:",oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    n=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['np']=n

    return render(request,'place_order.html',context)

def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    n=len(c)
    s=0
    for x in c:
        s=s+x.pid.price
    print(s)
    context={}
    context['np']=n
    context['total']=s
    context['products']=c
    return render(request,'cart.html',context)

def remove(request,cid): 
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def Remove(request,cid):
    o=Order.objects.filter(id=cid)
    o.delete()
    return redirect('/po')

def updateqty(request,qv,cid):
    # print()
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    s=0
    for x in c:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=c
    context['total']=s
    return render(request,'cart.html',context)

def about(request):
    # return HttpResponse("This is about page")
    return render(request,'about.html')

def contact(request):
    # return HttpResponse("This is contact page")
    return render(request,'contact.html')
def addition(request,a,b):
    print(type(a))
    res=int(a)+int(b)
    return HttpResponse(res)

def makepayment(request):
   orders=Order.objects.filter(uid=request.user.id)
   s=0
   for x in orders:
      s=s+x.pid.price*x.qty
      oid = x.order_id
   client = razorpay.Client(auth=("rzp_test_TQGla3PICQkrOo", "hG72sX4E0eQK21ePaCgg5R08"))
   data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
   payment = client.order.create(data=data)
   context={}
   context['data']=payment
   return render(request,'pay1.html',context)

def sendusermail(request):
    uemail=request.user.email
    send_mail(
    "Ekart oreder placed successfully",
    "order details",
    "pkandekar1@gmail.com",
    ["uemail"],
    fail_silently=False,
    )
    return HttpResponse("mail is send successfully")

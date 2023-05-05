from django.shortcuts import render,redirect
from django.views import View
from . models import Customer,Product,Cart,OrderPlaced
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import razorpay

class ProductView(View):
    def get(self,request):
        Bakery_and_Cookies=Product.objects.filter(category='BC')
        Snacks_and_Munchies=Product.objects.filter(category='SM')
        Fruits_and_Vegatables=Product.objects.filter(category='FV')
        Colddrink_and_Jucies=Product.objects.filter(category='CJ')
        return render(request,'app/home.html',{
            'Bakery_and_Cookies':Bakery_and_Cookies,'Snacks_and_Munchies':Snacks_and_Munchies,'Fruits_and_Vegatables':Fruits_and_Vegatables,'Colddrink_and_Jucies':Colddrink_and_Jucies})

class ProductDetailsView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        items_already_incart = False
        if request.user.is_authenticated:
            items_already_incart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

        return render(request,'app/productdetail.html',
        {'product':product,'items_already_incart':items_already_incart})

# ===================================== add_to_cart function ========================================
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')  

# ===================================== show_cart function ========================================
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temp_amount =(p.quantity*p.product.discounted_price)
                amount+=temp_amount
                totalamount = amount+shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'app/emptycart.html')

# ===================================== plus_cart function ========================================
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount = (p.quantity*p.product.discounted_price)
            amount+=temp_amount
        data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
            }
        return JsonResponse(data)

# ===================================== minus_cart fucntion ========================================

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount = (p.quantity*p.product.discounted_price)
            amount+=temp_amount
        data = {

                'quantity':c.quantity,
                'amount':amount,
                'totalamount':amount+shipping_amount
                }
        return JsonResponse(data)

# ===================================== remove_cart fucntion ========================================
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount = (p.quantity*p.product.discounted_price)
            amount+=temp_amount
        data = {
                'amount':amount,
                'totalamount':amount+shipping_amount
                }
        return JsonResponse(data)

# ===================================== buy_now fucntion ========================================
def buy_now(request):
    return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def about(request):
 return render(request, 'app/about.html')

# ===================================== address fucntion ========================================
# @login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

# ===================================== orders fucntion ========================================
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})

def Fruits_and_Vegetables(request,data=None):
    if data==None:
        Fruits_and_Vegetables=Product.objects.filter(category='FV')
    return render(request, 'app/Fruits_and_Vegetables.html',{'Fruits_and_Vegetables':Fruits_and_Vegetables})

def Colddrink_and_Jucies(request,data=None):
    if data==None:
        Colddrink_and_Jucies=Product.objects.filter(category='CJ')
    return render(request, 'app/Colddrink_and_Jucies.html',{'Colddrink_and_Jucies':Colddrink_and_Jucies})

def Bakery_and_Cookies(request,data=None):
    if data==None:
        Bakery_and_Cookies=Product.objects.filter(category='BC')
    return render(request, 'app/Bakery_and_Cookies.html',{'Bakery_and_Cookies':Bakery_and_Cookies})

def Snacks_and_Munchies(request,data=None):
    if data==None:
        Snacks_and_Munchies=Product.objects.filter(category='SM')
    return render(request, 'app/Snacks_and_Munchies.html',{'Snacks_and_Munchies':Snacks_and_Munchies})

# ===================================== CustomerRegistrationView class ========================================
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You Have Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

# ===================================== checkout fucntion ========================================
# @login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity*p.product.discounted_price)
            amount+=temp_amount
        totalamount = amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount, 'cart_items':cart_items,'discounted_price':p.product.discounted_price})

# ===================================== Payment_done function ========================================
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

    
# ===================================== ProfileView class ========================================
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


def payment(request):
        if request.method == 'Post':

            amount =50000
            currency ='INR'
            client =razorpay.client(
                auth=('rzp_test_iUWZFVE5ULJWhv','uGQJwyoJhJy2wGmeBPFyOyxe'))
            
            payment = client.order.create({'amount':amount, 'currency': 'INR', 'payment_capture':'1'}) 
     
        return render(request,'app/payment.html')
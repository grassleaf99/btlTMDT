from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'homepage/index.html')


class Register(View):
    def get(self, request):
        cu = CustomerForm()
        return render(request, 'register.html', {'cu':cu})

    def post(self, request):
        pcu = CustomerForm(request.POST)
        if pcu.is_valid():
            first_name = pcu.cleaned_data['first_name']
            mid_name = pcu.cleaned_data['mid_name']
            last_name = pcu.cleaned_data['last_name']
            email = pcu.cleaned_data['email']
            user_name = pcu.cleaned_data['username']
            pass_word = pcu.cleaned_data['password']
            repass_word = pcu.cleaned_data['repassword']
            phone = pcu.cleaned_data['phone']
            city = pcu.cleaned_data['city']
            district = pcu.cleaned_data['district']
            street = pcu.cleaned_data['street']
            houseNum = pcu.cleaned_data['houseNum']
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username taken')
                return redirect('name_register')
            elif Customer.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('name_register')
            elif pass_word != repass_word:
                messages.info(request, 'Password and confirm password do not match')
                return redirect('name_register')
            else:
                user = User.objects.create_user(username=user_name, password=pass_word)
                user.save()
                fullname = Fullname(firstName=first_name, midName=mid_name, lastName=last_name)
                fullname.save()
                address = Address(houseNum=houseNum, street=street, district=district, city=city)
                address.save()
                customer = Customer(user=user, fullname=fullname, address=address, phone=phone, email=email)
                customer.save()
                messages.success(request, 'Account was created for ' + user_name)
                return redirect('name_login')
        else:
            messages.info(request, 'Invalid sign up data')
            return redirect('name_register')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user_name = request.POST['un']
        #user_name = request.POST.get('un')
        pass_word = request.POST['pass']
        #pass_word = request.POST.get('pass')
        customer_user = authenticate(username=user_name, password=pass_word)
        if customer_user is not None:
            login(request, customer_user)
            return redirect('name_home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('name_login')


class HomeAfterLoginView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        customer = request.user.customer
        order, orderCreated = Order.objects.get_or_create(customer=customer, complete=False)
        cart, cartCreated = Cart.objects.get_or_create(order=order) # kiem tra order co cart ko, neu ko thi tao cart de order co the dung property get_cart_quantity
        #categorys = Category.objects.all()
        items = Item.objects.all()
        #context = {'categorys':categorys, 'cart':cart}
        context = {'items':items, 'cart':cart}
        return render(request, 'home.html', context)

class ViewCart(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        customer = request.user.customer
        order, orderCreated = Order.objects.get_or_create(customer=customer, complete=False)
        cart, cartCreated = Cart.objects.get_or_create(order=order)
        itemcarts = cart.itemcart_set.all()
        context = {'itemcarts':itemcarts, 'cart':cart}
        return render(request, 'cart.html', context)

class ViewCheckout(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart, cartCreated = Cart.objects.get_or_create(order=order)
        itemcarts = cart.itemcart_set.all()
        context = {'itemcarts': itemcarts, 'cart':cart, 'order': order, 'customer':customer}
        return render(request, 'checkout.html', context)

class Logout(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        logout(request)
        return redirect('index')

def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    print('Action: ', action)
    print('itemId: ', itemId)

    customer = request.user.customer
    item = Item.objects.get(id=itemId)
    order, orderCreated = Order.objects.get_or_create(customer=customer, complete=False)
    cart, cartCreated = Cart.objects.get_or_create(order=order)
    itemcart, itemcartCreated = ItemCart.objects.get_or_create(cart=cart, item=item) # dung get_or_create de kiem tra xem itemcart da ton tai chua, tranh viec tao lai itemcart

    if action == 'add':
        itemcart.quantity = itemcart.quantity + 1
    elif action == 'remove':
        itemcart.quantity = itemcart.quantity - 1

    itemcart.save()

    if itemcart.quantity <= 0:
        itemcart.delete() # xoa itemcart khoi cart

    return JsonResponse('Cart was updated', safe=False)

@csrf_exempt # ko can csrf van post du lieu duoc
def processOrder(request):
    print('JSON: ', request.body)
    dataJSON = json.loads(request.body)
    totalPrice = float(dataJSON['totalPrice'])
    first_name = dataJSON['my-first-name']
    mid_name = dataJSON['my-mid-name']
    last_name = dataJSON['my-last-name']
    city = dataJSON['my-city']
    district = dataJSON['my-district']
    street = dataJSON['my-street']
    houseNum = dataJSON['my-house-number']
    phone = dataJSON['my-phone']
    print(first_name)
    print(mid_name)
    print(last_name)
    print(city)
    print(district)
    print(street)
    print(houseNum)
    print(phone)
    print(totalPrice)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if totalPrice == order.totalOrderPrice:  # kiem tra user co gian lan bang cach thay doi tong tien cua cart ko
        order.complete = True
        order.save()
        print('Order successfully')
        return JsonResponse('Order completed', safe=False)

def bua(request):
    return render(request, 'homepage/base.html')
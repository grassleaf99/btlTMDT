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
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            if Employee.objects.filter(user=user).exists():
                employee = Employee.objects.get(user=user)
                if SaleStaff.objects.filter(employee=employee).exists():
                    return redirect('name_em_home')
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
        categories = Category.objects.all()
        #items = Item.objects.all()
        context = {'categories':categories, 'cart':cart}
        #context = {'items':items, 'cart':cart}
        return render(request, 'home.html', context)

class SearchResult(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        rex = request.POST['BoEC']
        items = Item.objects.filter(name__contains=rex)
        context = {'items':items, 'rex':rex}
        return render(request, 'search.html', context)


class EmAfterLoginView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        salestaff = request.user.employee.salestaff
        return render(request, 'emHome.html')

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
    customer = request.user.customer
    fullname = customer.fullname
    address = customer.address
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
    pay = dataJSON['type_pay']
    print(first_name)
    print(mid_name)
    print(last_name)
    print(city)
    print(district)
    print(street)
    print(houseNum)
    print(phone)
    print(totalPrice)
    print(pay)
    if fullname.firstName != first_name:
        fullname.firstName = first_name
        fullname.save()
    if fullname.midName != mid_name:
        fullname.midName = mid_name
        fullname.save()
    if fullname.lastName != last_name:
        fullname.lastName = last_name
        fullname.save()
    if address.city != city:
        address.city = city
        address.save()
    if address.district != district:
        address.district = district
        address.save()
    if address.street != street:
        address.street = street
        address.save()
    if address.houseNum != houseNum:
        address.houseNum = houseNum
        address.save()
    if customer.phone != phone:
        customer.phone = phone
        customer.save()
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    if totalPrice == order.totalOrderPrice:  # kiem tra user co gian lan bang cach thay doi tong tien cua cart ko
        order.complete = True
        paypal = Payment.objects.get(name='CreditCard')
        order.payment = paypal
        order.save()
        print('Order successfully')
        return JsonResponse('Order completed', safe=False)

def processNhan(request):
    customer = request.user.customer
    fullname = customer.fullname
    address = customer.address
    first_name = request.POST['my-first-name']
    mid_name = request.POST['my-mid-name']
    last_name = request.POST['my-last-name']
    city = request.POST['my-city']
    district = request.POST['my-district']
    street = request.POST['my-street']
    houseNum = request.POST['my-house-number']
    phone = request.POST['my-phone']
    if fullname.firstName != first_name:
        fullname.firstName = first_name
        fullname.save()
    if fullname.midName != mid_name:
        fullname.midName = mid_name
        fullname.save()
    if fullname.lastName != last_name:
        fullname.lastName = last_name
        fullname.save()
    if address.city != city:
        address.city = city
        address.save()
    if address.district != district:
        address.district = district
        address.save()
    if address.street != street:
        address.street = street
        address.save()
    if address.houseNum != houseNum:
        address.houseNum = houseNum
        address.save()
    if customer.phone != phone:
        customer.phone = phone
        customer.save()
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order.complete = True
    payNhan = Payment.objects.get(name='Receive')
    order.payment = payNhan
    order.save()
    print('Order successfully')
    messages.info(request, 'Order successfully')
    return redirect('name_home')

class ViewAllOrders(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = request.user
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            if SaleStaff.objects.filter(employee=employee).exists():
                completedOrders = Order.objects.filter(complete=True, confirmOrder=False)
                context = {'orders': completedOrders}
                return render(request, 'allorders.html', context)
        customer = user.customer
        confirmedOrders = Order.objects.filter(customer=customer, complete=True, confirmOrder=True)
        context = {'orders': confirmedOrders}
        return render(request, 'allCCorders.html', context)

class DetailOrder(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, order_id):
        user = request.user
        order = Order.objects.get(pk=order_id)
        context = {'order': order}
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            if SaleStaff.objects.filter(employee=employee).exists():
                return render(request, 'confirmOrder.html', context)


class ConfirmOrder(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        # du input voi name order-id nhan du lieu la number nhung sau do khi lay ve tu request.POST thi du lieu lai la kieu xau (str) nen can chuyen sang kieu int
        orderID = int(request.POST['order-id'])
        order = Order.objects.get(pk=orderID)
        order.saleStaff = request.user.employee.salestaff
        order.confirmOrder = True
        order.save()
        messages.info(request, 'Order with ID ' + str(orderID) + ' has been confirmed')
        return redirect('name_em_home')

class CreateUpdateComment(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        comment, created = Comment.objects.get_or_create(order=order)
        context = {'comment':comment}
        return render(request, 'cuComment.html', context)

class PostCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        commentID = int(request.POST['comment-id'])
        comment = Comment.objects.get(pk=commentID)
        comment.content = request.POST['content']
        comment.save()
        return redirect('name_allcomment')

class AllCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = request.user
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            if SaleStaff.objects.filter(employee=employee).exists():
                comments = Comment.objects.all()
                context = {'comments':comments}
                return render(request, 'chooseComment.html', context)
        customer = user.customer
        orders = Order.objects.filter(customer=customer)
        context = {'orders':orders}
        return render(request, 'allcomments.html', context)

class CreateUpdateReply(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, comment_id):
        saleStaff = request.user.employee.salestaff
        comment = Comment.objects.get(pk=comment_id)
        reply, created = Reply.objects.get_or_create(comment=comment, saleStaff=saleStaff)
        context = {'reply': reply}
        return render(request, 'cuReply.html', context)

class PostReplyView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        replyID = int(request.POST['reply-id'])
        reply = Reply.objects.get(pk=replyID)
        reply.content = request.POST['content']
        reply.save()
        return redirect('name_allreply')

class AllReplyView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        user = request.user
        if Employee.objects.filter(user=user).exists():
            employee = Employee.objects.get(user=user)
            if SaleStaff.objects.filter(employee=employee).exists():
                saleStaff = SaleStaff.objects.get(employee=employee)
                replies = Reply.objects.filter(saleStaff=saleStaff)
                context = {'replies': replies}
                return render(request, 'allreply.html', context)

class RepliesOfComment(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        replies= Reply.objects.filter(comment=comment)
        context = {'replies':replies}
        return render(request, 'dtReplies.html', context)

def bua(request):
    return render(request, 'homepage/base.html')
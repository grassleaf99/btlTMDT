from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='name_register'),
    path('login/', views.Login.as_view(), name='name_login'),
    path('home/', views.HomeAfterLoginView.as_view(), name='name_home'),
    path('cart/', views.ViewCart.as_view(), name='name_cart'),
    path('checkout/', views.ViewCheckout.as_view(), name='name_checkout'),
    path('logout/', views.Logout.as_view(), name='name_out'),
    path('updateItem/', views.updateItem, name='name_updateitem'),
    path('processOrder/', views.processOrder, name='name_processOder'),
    path('processNhan/', views.processNhan, name='name_processNhan'),
    path('allOrders/', views.ViewAllOrders.as_view(), name='name_allorders'),
    path('bua/', views.bua, name='bua'),
]

# tai khoan 1: test test
# tai khoan 2: test2 test2
# tai khoan 3: test3 test3
# tai khoan 4: test4 test4
# ...
# tai khoan employee sale: sale SaleStaff

from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='name_register'),
    path('login/', views.Login.as_view(), name='name_login'),
    path('home/', views.HomeAfterLoginView.as_view(), name='name_home'),
    path('logout/', views.Logout.as_view(), name='name_out'),
    path('bua/', views.bua, name='bua'),
]

# tai khoan 1: test test
# tai khoan 2: test2 test2
# tai khoan 3: test3 test3
# tai khoan 4: test4 test4

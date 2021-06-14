from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='name_register'),
    path('login/', views.Login.as_view(), name='name_login'),
    path('home/', views.HomeAfterLoginView.as_view(), name='name_home'),
    path('search/', views.SearchResult.as_view(), name='name_search'),
    path('emHome/', views.EmAfterLoginView.as_view(), name='name_em_home'),
    path('cart/', views.ViewCart.as_view(), name='name_cart'),
    path('checkout/', views.ViewCheckout.as_view(), name='name_checkout'),
    path('logout/', views.Logout.as_view(), name='name_out'),
    path('updateItem/', views.updateItem, name='name_updateitem'),
    path('processOrder/', views.processOrder, name='name_processOder'),
    path('processNhan/', views.processNhan, name='name_processNhan'),
    path('allOrders/', views.ViewAllOrders.as_view(), name='name_allorders'),
    path('detailOrder/<int:order_id>', views.DetailOrder.as_view(), name='name_dtOd'),
    path('confirmOrder/', views.ConfirmOrder.as_view(), name='name_cfOd'),
    path('cuComment/<int:order_id>', views.CreateUpdateComment.as_view(), name='name_cucomment'),
    path('postComment/', views.PostCommentView.as_view(), name='name_postcomment'),
    path('allComments/', views.AllCommentView.as_view(), name='name_allcomment'),
    path('cuReply/<int:comment_id>', views.CreateUpdateReply.as_view(), name='name_cuReply'),
    path('postReply/', views.PostReplyView.as_view(), name='name_postreply'),
    path('allReplies/', views.AllReplyView.as_view(), name='name_allreply'),
    path('dtReplies/<int:comment_id>', views.RepliesOfComment.as_view(), name='name_dtRp'),
    path('bua/', views.bua, name='bua'),
]

# tai khoan 1: test test
# tai khoan 2: test2 test2
# tai khoan 3: test3 test3
# tai khoan 4: test4 test4
# ...
# tai khoan employee sale: sale SaleStaff

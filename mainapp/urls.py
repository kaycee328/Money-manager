from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage2.as_view(), name='home' ),
    path('home/', views.Homepage.as_view(), name='homepage' ),
    path('home2/', views.Homepage2.as_view(), name='homepage2' ),
    path('home3/', views.Homepage3.as_view(), name='homepage3' ),
    path('transaction/new/', views.CreateTransaction.as_view(), name='create' ),
    path('edit/<int:pk>/', views.EditTransaction.as_view(), name='edit' ),
    path('delete/transactions/', views.DeleteTransaction.as_view(), name='delete' ),
    # path('delete/transactions/<int:pk>/', views.DeleteTransaction.as_view(), name='confirm-delete' ),
    
    path('view/<int:pk>/', views.TransactionDetails.as_view(), name='transaction-detail' ),
    path('create/', views.CreateTransaction.as_view(), name='create' ),
    path('mytransactions/list/', views.TransactionList.as_view(), name='my-transactions' ),
    path('mytransactions2/list/', views.TransactionList.as_view(), name='my-transactions2' ),
    # path('', views.HomePageView.as_view(), name='home' ),
    # path('home/', views.homepage, name='homepage' ),

    # AUTHENTICATION LINKS
    path('signup/', views.register, name='signup' ),
    path('login/', views.UserLogin.as_view(), name='user-login' ),
    path('logout/', views.LogoutUser.as_view(), name='user-logout' ),
    path('api/', views.jsonfile, name='json' ),

]


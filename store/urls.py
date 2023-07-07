from pathlib import Path
from django.contrib import admin
from django.urls import path
from .views import Index ,  Login , Signup , logout , Cart , checkout , orders

urlpatterns = [
    path('', Index.as_view() , name='homepage'),
    path('signup', Signup.as_view()  , name="signup" ) , 
    path('login', Login.as_view() , name="login" ),
    path('logout', logout , name="logout" ),
    path('cart', Cart.as_view() , name="cart" ),
    path('check-out', checkout.as_view() , name="checkout" ),
    path('orders', orders.as_view() , name="orders" )
]

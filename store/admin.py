from math import prod
from unicodedata import category
from django.contrib import admin
from . models import Product , Category , Customer  , Orders

# Register your models here.
class AdminProduct(admin.ModelAdmin):
    list_display = ['name','price','category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['First_name','last_name','phone','email']

class OrdersAdmin(admin.ModelAdmin):
    list_display = ['customer' , 'product' , 'quantity' , 'price' , 'address','mobile','date']


admin.site.register(Product , AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Customer , CustomerAdmin)
admin.site.register(Orders, OrdersAdmin)
import email
from itertools import product
from pyexpat import model
from unicodedata import category
from django.db import models
from datetime import datetime


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey("Category" , on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , blank=True)
    image = models.ImageField(upload_to='uplodas/products/')

    @staticmethod
    def get_all_product():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category_ID(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_product()

    @staticmethod
    def get_product_by_id(product_list_id):
        return Product.objects.filter(id__in  = product_list_id)

class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_category():
        return Category.objects.all()

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    First_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)

    def register(self):
        self.save()

    def isexist(self):
        if Customer.objects.filter(email = self.email):
            return True
        return False

    @staticmethod
    def GetUser(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False

        
class Orders(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=500)
    mobile = models.CharField(max_length=500)
    date = models.DateTimeField(default= datetime.today )
    completed = models.BooleanField(default=False)


    def PlaceOrder(self):
        self.save()
    
    @staticmethod
    def Orders_by_customerID(customer_id):
        return Orders.objects.filter(customer = customer_id).order_by("-date")


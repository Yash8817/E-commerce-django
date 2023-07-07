from distutils.log import error
from distutils.sysconfig import customize_compiler
import http
from itertools import product
from math import prod
from operator import methodcaller
from unicodedata import category
from wsgiref.validate import validator
from django.shortcuts import render, redirect , HttpResponseRedirect
from django.http import HttpResponse
from .models import Orders, Product, Category, Customer, Orders
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from django.core.mail import send_mail , EmailMultiAlternatives
from email.message import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


# Create your views here.

class Index(View):

    def post(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')

        cart = request.session.get('cart')

        if cart:
            qty = cart.get(product_id)
            if qty:
                if remove:

                    if qty <= 1:
                        cart.pop(product_id)
                    else:
                        cart[product_id] -= 1

                else:
                    cart[product_id] += 1
            else:
                cart[product_id] = 1

        else:
            cart = {}
            cart[product_id] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        cart = request.session.get('cart')

        if not cart:
            request.session['cart'] = {}

        prds = None
        categoryId = request.GET.get('category')
        if categoryId:
            prds = Product.get_all_product_by_category_ID(categoryId)
        else:
            prds = Product.get_all_product()

        Categories = Category.get_all_category()
        data = {
            'prds': prds,
            'Categories': Categories
        }
        return render(request, "index.html", data)


class Signup(View):

    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        PostData = request.POST
        fname = PostData.get("fname")
        lname = PostData.get("lname")
        email = PostData.get("email")
        password = PostData.get("password")
        mobile = PostData.get("mobile")

        values = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'password': password,
            'mobile': mobile
        }
        # creating customer model object
        customer = Customer(First_name=fname, last_name=lname,
                            phone=mobile, password=password, email=email)

        # validation
        error_message = self.ValidateCustomer(customer)

        # is no error is there then create customer
        if not error_message:
            # hash password
            customer.password = make_password(customer.password)
            customer.register()

        #     # sending email mesage
        #     current_site = get_current_site(request)
        #     email_subject = "Your Account is Ready - Get Started Now"
        #     email_message = render_to_string("email.html", {
        #         'username' : fname , 
        #         'useremail' : email , 
        #         'password' : password , 
        #         'current_site' : current_site
        #     })
        #     eml = EmailMessage(
        #     email_subject , 
        #     email_message , 
        #     'praticepython@gmail.com' , 
        #     [email],
        # )
        #     eml.fail_silently=False 
        #     eml.send_mail()


            email_subject = "Your Account is Ready - Get Started Now"
            email_message = "Hi "+ str(fname)  + ",\n We can’t wait for you to start using Eshop  and seeing results in your business.\nSimply go here 127.0.0.1:8000 to get started, or visit to learn more about how to use .\nAs always, our support team can be reached at practicepython@gmail.com if you ever get stuck.\nHave a great day!"
            from_email = 'praticepython@gmail.com'
            to_email = [email]

            send_mail(email_subject , email_message , from_email , to_email , fail_silently=True)


            return redirect('homepage')
        else:
            data = {
                'values': values,
                'error': error_message
            }
            return render(request, "signup.html", data)

    def ValidateCustomer(self, customer):
        error_message = None
        if not customer.First_name:
            error_message = "First name required !"
        elif not customer.last_name:
            error_message = "Last name required !"
        elif not customer.email:
            error_message = "email required !"
        elif len(customer.email) < 4:
            error_message = "invalid email !"
        elif not customer.password:
            error_message = "password required !"
        elif len(customer.password) < 8:
            error_message = "password should be grater than 8 character !"
        elif not customer.phone:
            error_message = "mobile required !"
        elif len(customer.phone) < 10:
            error_message = "invalid mobile !"
        elif customer.isexist():
            error_message = "Email already exist !"


class Login(View):
    returnURL  = None
    def get(self, request):
        Login.returnURL = request.GET.get('returnURL')
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # check if customer exist if there then get the object
        customer = Customer.GetUser(email)

        error_message = None
        if customer:
            # validate password
            flag = check_password(password, customer.password)

            # if password match
            if flag:
                request.session['customer'] = customer.id

                if Login.returnURL:
                    return HttpResponseRedirect(Login.returnURL)
                else:
                    Login.returnURL = None
                    return redirect("homepage")
            else:
                error_message = "Email address or passwprd is invalid !"
                return render(request, "login.html", {'error': error_message})

        else:
            error_message = "Email not exist !"
            return render(request, "login.html", {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        product_list = list(request.session.get('cart'))
        product_data = Product.get_product_by_id(product_list)
        return render(request, "cart.html", {'product_data': product_data})


class checkout(View):
    @method_decorator(auth_middleware)
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get("customer")
        cart = request.session.get("cart")
        product_list = list(request.session.get('cart'))
        product_data = Product.get_product_by_id(product_list)

        for product in product_data:
            order = Orders(product=product,
                           customer=Customer(id=customer),
                           quantity=cart.get(str(product.id)),
                           price=product.price,
                           address=address,
                           mobile=phone)

            order.PlaceOrder()
        request.session['cart'] = {}
        return redirect("/cart")




class orders(View):
    

    @method_decorator(auth_middleware)
    def get(self , request):
        customer = request.session.get("customer")
        order_data = Orders.Orders_by_customerID(customer)
        return render(request , "orders.html" , {'order_data':order_data})

from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .forms import LoginForm,SignUpForm
from django.contrib.auth import authenticate,logout,login
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from Accounts.models import User
from Home.models import Customer
from API.signals import merge_guest_cart_to_user
@method_decorator(cache_control(no_store = True,no_cache=True), name='dispatch')

class Login(View):
    def get(self,request):
        return render(request,"authentication/login.html")
    
    def post(self,request,*args, **kwargs):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user  = authenticate(request,email=email,password = password)
            if user is not None:
                login(request,user)
                customer,created = Customer.objects.get_or_create(customer = request.user)
                
                # Merge guest cart with user cart if guest_id exists
                guest_id = request.session.get('guest_id')
                if guest_id:
                    merge_guest_cart_to_user(user, guest_id)
                
                return redirect("home")
            else:
                return redirect("login")
        return render(request, "account/login.html", {"errors": form.errors})
@method_decorator(cache_control(no_store = True,no_cache=True), name='dispatch')
class Signup(View):
    def get(self,request):
        return render(request,"authentication/signup.html")
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = User(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("username"),
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            # customer = Customer.objects.create(customer=user.email)
            auth_user = authenticate(request,username = form.cleaned_data.get("email"),password = form.cleaned_data.get("password"))
            login(request, user)
            
            # Merge guest cart with user cart if guest_id exists
            guest_id = request.session.get('guest_id')
            if guest_id:
                merge_guest_cart_to_user(user, guest_id)
            
            return redirect("/")
            
        else:
         
            if 'email' in form.errors:
                return render(request, "authentication/signup.html", {"errors1": form.errors['email']})
            elif 'username' in form.errors:
                return render(request, "authentication/signup.html", {"errors2": form.errors['username']})
            elif 'password' in form.errors:
                return render(request, "authentication/signup.html",{"errors3": form.errors['password']})
            elif 'confirm_password' in form.errors:
                return render(request, "authentication/signup.html",{"errors4": form.errors['confirm_password']})
                
                

@method_decorator(cache_control(no_store = True,no_cache=True), name='dispatch')

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("login")

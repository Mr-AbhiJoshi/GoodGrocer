from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import  productCategory, productSubcategory, productItem
#from .forms import <Your form names>


# Create your views here.
def home(request):
    category = productCategory.objects.all()
    context = {'category':category}
    return render(request, 'home.html', context)

def loginUser(request):
    user_exists = 'yes'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not found')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not match')
    
    context = {'user_exists':user_exists}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    
    context = {'form':form}
    return render(request, 'login_register.html', context)

def shop(request):
    categories = productCategory.objects.all()
    subcategories = productSubcategory.objects.all()
    products = productItem.objects.all()
    onDealProducts = productItem.objects.filter(onDeal=True)
    context = {'categories':categories, 'subcategories':subcategories, 'products':products, 'onDealProducts':onDealProducts}
    return render(request, 'shop.html', context)

def product(request, pk):
    context = {}
    return render(request, 'product.html', context)

@login_required(login_url='login')
def cart(request):
    context = {}
    return render(request, 'cart.html', context)

def learn(request):
    context = {}
    return render(request, 'learn.html', context)
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

def shopPage(request):
    page = 'shop'
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    
    products = productItem.objects.filter(
        Q(subcategory__category__name__icontains = q) |
        Q(subcategory__name__icontains = q) |
        Q(name__icontains = q)
    )
    
    categories = productCategory.objects.all()
    subcategories = productSubcategory.objects.all()
    product_count = products.count()
    #onDealProducts = productItem.objects.filter(onDeal=True)
    context = {'page':page, 'categories':categories, 'subcategories':subcategories, 'products':products, 'product_count':product_count}
    return render(request, 'shop.html', context)

def productDisplay(request, pk):
    context = {}
    return render(request, 'product_display.html', context)

@login_required(login_url='login')
def cartPage(request):
    context = {}
    return render(request, 'cart.html', context)

def learnPage(request):
    context = {}
    return render(request, 'learn.html', context)

def dealsPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    
    onDealProducts = productItem.objects.filter(onDeal=True)
    products = onDealProducts.filter(
        Q(subcategory__name__icontains = q) |
        Q(name__icontains = q)
    )
    
    categories = productCategory.objects.all()
    subcategories = productSubcategory.objects.all()
    product_count = products.count()
    context = {'categories':categories, 'subcategories':subcategories, 'products':products, 'product_count':product_count}
    return render(request, 'deals.html', context)
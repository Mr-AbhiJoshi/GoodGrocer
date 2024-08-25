from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import  productCategory, productSubcategory, productItem, Cart, CartItem, Contact
from .forms import ContactForm
import uuid


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
            return redirect('login')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password does not match')
    
    context = {'user_exists':user_exists}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration. Please ensure you are filling the form correctly!')
            
    else:
        form = UserCreationForm()
    
    context = {'form':form}
    return render(request, 'login_register.html', context)

@login_required(login_url='login')
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
    givenProduct = productItem.objects.get(id=pk)
    context = {'product':givenProduct}
    return render(request, 'product_display.html', context)

@login_required(login_url='login')
def cartPage(request, pk):
    givenUser = User.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(user=givenUser)
    cartItems = cart.cartitem_set.all()
    total_price = sum(item.total_price() for item in cartItems)

    context = {
        'cartItems': cartItems,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)

def learnPage(request):
    context = {}
    return render(request, 'learn.html', context)

def contactUs(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been delivered.')
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'contact.html', context)

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

@login_required(login_url='login')
def addToCart(request, pk):
    product = productItem.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cartItems = cart.cartitem_set.all()
    total_price = sum(item.total_price() for item in cartItems)

    context = {'cart_active': True, 'cartItems': cartItems, 'total_price': total_price}
    return render(request, 'cart.html', context)

def removeFromCart(request, pk):
    givenProduct = productItem.objects.get(id=pk)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(cart=cart, product=givenProduct)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart', request.user.id)

def clearCart(request, pk):
    givenUser = User.objects.get(id=pk)
    cart = Cart.objects.get(user=givenUser)
    
    if cart:
        cart.delete()

    return redirect('cart', request.user.id)

def checkoutPage(request, pk):
    if request.method == 'POST':
        givenUser = User.objects.get(id=request.user.id)
        cart = Cart.objects.get(user=givenUser)
    
        if cart:
            cart.delete()
        
        return redirect('orderPlaced')
    
    givenUser = User.objects.get(id=pk)
    cart, created = Cart.objects.get_or_create(user=givenUser)
    cartItems = cart.cartitem_set.all()
    total_price = sum(item.total_price() for item in cartItems)
    total_items = cartItems.count()
    
    context = {
        'cartItems': cartItems, 'total_price': total_price, 'total_items':total_items}
    
    return render(request, 'checkout.html', context)

def orderPlaced(request):
    uuid_part = str(uuid.uuid4())[:8]
    order_id = f"{uuid_part}"
    context = {'order_id':order_id}
    return render(request, 'order_placed.html', context)
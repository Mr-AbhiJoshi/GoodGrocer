from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('login/', views.loginUser, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('register/', views.registerUser, name="register"),
	path('shop/', views.shopPage, name="shop"),
	path('product/<str:pk>', views.productDisplay, name="product"),
	path('cart/<str:pk>', views.cartPage, name="cart"),
	path('learn/', views.learnPage, name="learn"),
	path('contact/', views.contactUs, name="contact"),
	path('deals/', views.dealsPage, name="deals"),
	path('addToCart/<str:pk>', views.addToCart, name="addToCart"),
 	path('removeFromCart/<str:pk>', views.removeFromCart, name="removeFromCart"),
 	path('clearCart/<str:pk>', views.clearCart, name="clearCart"),
 	path('checkout/<str:pk>', views.checkoutPage, name="checkout"),
 	path('orderPlaced/', views.orderPlaced, name="orderPlaced"),
]

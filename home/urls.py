from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('login/', views.loginUser, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('register/', views.registerUser, name="register"),
	path('shop/', views.shopPage, name="shop"),
	path('product/<str:pk>', views.productDisplay, name="product"),
	path('cart/', views.cartPage, name="cart"),
	path('learn/', views.learnPage, name="learn"),
	path('deals/', views.dealsPage, name="deals"),
]

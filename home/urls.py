from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('login/', views.loginUser, name="login"),
	path('logout/', views.logoutUser, name="logout"),
	path('register/', views.registerUser, name="register"),
	path('shop/', views.shop, name="shop"),
	path('product/<str:pk>', views.product, name="product"),
	path('cart/', views.cart, name="cart"),
	path('learn/', views.learn, name="learn"),
]

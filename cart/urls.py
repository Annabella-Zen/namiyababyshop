from django.urls import path
from cart import views


app_name = 'cart'
urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart-remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart_add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('checkout/', views.checkout, name='checkout'),
    path('result/', views.checkout, name='result'),
]

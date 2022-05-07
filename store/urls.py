from django.urls import path
from store import views


app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('subcategory/<int:pk>/', views.subcategory, name='subcategory'),
    path('subcategory2/<int:pk>/', views.subcategory2, name='subcategory2'),
    path('product-detail/<int:product_id>/', views.product_detail, name='product-detail'),
    path('products-service/', views.products_service, name='products_service'),
    path('products-service/<int:pk>/', views.product_service, name='product_service'),
    # path('blog/', views.blog, name='blog'),
    path('search/', views.search, name='search'),
]

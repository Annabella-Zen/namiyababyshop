from django.urls import path
from socialShare import views


app_name = 'socialShare'
urlpatterns = [
    path('home/', views.home, name='home')
]

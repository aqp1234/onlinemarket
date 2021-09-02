from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', index, name='index'),
    path('add_cart/<int:product_id>/', add_cart, name='add_cart'),
    path('delete_cart/<int:product_id>/', delete_cart, name='delete_cart'),
]
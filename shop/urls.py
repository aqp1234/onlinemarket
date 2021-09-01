from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', index, name='index'),
    path('add_product/', add_product, name='add_product'),
    path('detail_product/<int:product_id>', detail_product, name='detail_product'),
    path('update_product/<int:product_id>', update_product, name='update_product'),
    path('delete_product/<int:product_id>', delete_product, name='delete_product'),
]
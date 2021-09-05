from django.urls import path
from .views import *

app_name = 'review'

urlpatterns = [
    path('add_review/<int:product_id>/', add_review, name='add_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
]
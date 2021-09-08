from django.urls import path
from .views import *

app_name = 'qna'

urlpatterns = [
    path('add_question/<int:product_id>', add_question, name='add_question'),
]
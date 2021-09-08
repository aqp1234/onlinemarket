from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from shop.models import Product
from .models import Question, Answer
from .forms import AddQuestionForm

# Create your views here.
def add_question(request, product_id):
    product = Product.objects.get(id=product_id)
    login_user = request.user
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            _question = Question.objects.create(user=login_user, product=product, title=cd['title'], question=cd['question'], is_secret=cd['is_secret'])
            _question.save()
            return redirect('shop:detail_product', product_id=product_id)
        return render(request, 'qna/add_question.html',{'form': form})
    else:
        form = AddQuestionForm()
        return render(request, 'qna/add_question.html',{'form': form})

    
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import *

# Create your views here.
def index(request):
    products = Product.objects.filter(available_display=True)
    return render(request, 'shop/index.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            category = Category.objects.get(id=cd['category'])
            new_product = Product(
                user=request.user,
                category=category,
                name=cd['name'],
                image=cd['image'],
                description=cd['description'],
                meta_description=cd['meta_description'],
                price=cd['price'],
                stock=cd['stock'],
                available_display=cd['available_display'],
                available_order=cd['available_order'],
            )
            new_product.save()
            return redirect('/')
        else:
            return render(request, 'shop/add_product.html', {'form': form})
    else:
        form = ProductForm()
        return render(request, 'shop/add_product.html', {'form': form})

def detail_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/detail_product.html', {'product': product})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.user != request.user:
        return redirect('/')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            category = Category.objects.get(id=cd['category'])
            product = Product(
                user=request.user,
                category=category,
                name=cd['name'],
                image=cd['image'],
                description=cd['description'],
                meta_description=cd['meta_description'],
                price=cd['price'],
                stock=cd['stock'],
                available_display=cd['available_display'],
                available_order=cd['available_order'],
            )
            product.save()
            return redirect('/detail_product/' + product_id)
        else:
            return render(request, 'shop/update_product.html', {'form': form})
    else:
        form = ProductForm(initial=product.__dict__)
        return render(request, 'shop/update_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    else:
        return render(request, 'shop/delete_product.html', {'product': product})


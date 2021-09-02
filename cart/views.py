from django.shortcuts import render, redirect
from .models import Cart, CartItem
from shop.models import Product

# Create your views here.
def index(request):
    login_user = request.user
    try:
        user_cart = Cart.objects.get(user=login_user)
    except Cart.DoesNotExist:
        user_cart = Cart.objects.create(user=login_user)
    cartitems = user_cart.cartitems.all()
    return render(request, 'cart/index.html', {'cartitems': cartitems, 'cart':user_cart})

def add_cart(request, product_id):
    login_user = request.user
    product = Product.objects.get(id=product_id)
    try:
        user_cart = Cart.objects.get(user=login_user)
    except Cart.DoesNotExist:
        user_cart = Cart.objects.create(user=login_user)
    
    try:
        cartitem = CartItem.objects.get(cart=user_cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
    except CartItem.DoesNotExist:
        cartitem = CartItem.objects.create(
            product=product,
            cart=user_cart,
            quantity=1,
        )
        cartitem.save()
    return redirect('cart:index')

def delete_cart(request, product_id):
    login_user = request.user
    try:
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(user=login_user)
        cartitem = CartItem.objects.get(cart=cart,product=product)
        cartitem.delete()
    except CartItem.DoesNotExist:
        redirect('cart:index')
    except Cart.DoesNotExist:
        redirect('cart:index')
    except Product.DoesNotExist:
        redirect('cart:index')
    return redirect('cart:index')


from django.shortcuts import render, redirect
from shop.models import Product
from .models import Review
# Create your views here.
def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    user = request.user
    review = request.POST.get('review')
    new_review = Review.objects.create(user=user, product=product, review=review)
    new_review.save()
    return redirect('shop:detail_product', product_id=product_id)

def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect('shop:detail_product', product_id=review.product.id)
from django.shortcuts import render

from .cart import Cart
from products.models import Tree
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

def cart_summary(request):
    return render(request, 'cart/cart_summary.html')

def cart_add(request):
    # get the cart
    cart = Cart(request)

    # test for post | 'post' we set in template script
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Tree, id=product_id)
        cart.add(product)
        return JsonResponse({'Product Name': product.name})

def cart_delete(request):
    pass

def cart_update(request):
    pass
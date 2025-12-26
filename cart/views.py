from django.shortcuts import render

from .cart import Cart
from products.models import Tree
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    
    context = {
        'cart_items': cart_items,
        # 'cart_total': cart.get_total_price(),
        'cart_count': len(cart),
    }
    return render(request, 'cart/cart_summary.html', context)


def cart_add(request):
    # get the cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Tree, id=product_id)
        
        try:
            cart.add(product)
            return JsonResponse({
                'success': True,
                'product_name': product.name,
                'cart_count': len(cart)
            })
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Tree, id=product_id)
        
        if str(product_id) in cart.cart:
            cart.remove(product)
            return JsonResponse({
                'success': True,
                'removed_product': product.name,
                'cart_count': len(cart),
                'cart_total': cart.get_total_price()
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Product not in cart'
            }, status=400)



def cart_update(request):
    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Tree, id=product_id)
        
        try:
            cart.update(product, quantity)  # inside goes check of quantity
            
            # Get updated item data
            item = cart.cart.get(str(product_id))
            item_total = float(item['price']) * item['quantity'] if item else 0
            
            return JsonResponse({
                'success': True,
                'quantity': quantity,
                'item_total': item_total,
                'cart_total': cart.get_total_price(),
                'cart_count': len(cart)
            })
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
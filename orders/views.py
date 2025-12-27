from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ShippingAddress, Order, OrderItem
from .forms import ShippingAddressForm, OrderForm, OrderPlacementForm
from cart.cart import Cart
from products.models import Tree

@login_required  # automatically redirects to login page as used 'django.contrib.auth.urls'
def add_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('users:home')
    else:
        form = ShippingAddressForm()
    return render(request, 'orders/shipping_address_form.html', {'form': form})


@login_required
def delete_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    address.delete()
    return redirect('users:home')


@login_required
def update_address(request, pk):
    address = get_object_or_404(ShippingAddress, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('users:home')
    else:
        form = ShippingAddressForm(instance=address)
    return render(request, "orders/shipping_address_form.html", {"form": form})


from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages

def place_order(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()

    if not cart_items:
        return redirect('cart:cart_summary')

    if request.method == 'POST':
        form = OrderPlacementForm(
            request.POST,
            user=request.user if request.user.is_authenticated else None
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Shipping address
                    existing_address = form.cleaned_data.get('existing_address')

                    if existing_address:
                        shipping_address = existing_address
                    else:
                        shipping_address = ShippingAddress.objects.create(
                            user=request.user if request.user.is_authenticated else None,
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            address1=form.cleaned_data['address1'],
                            address2=form.cleaned_data.get('address2', ''),
                            city=form.cleaned_data['city'],
                            state=form.cleaned_data['state'],
                            postal_code=form.cleaned_data['postal_code'],
                            country=form.cleaned_data['country'],
                            phone=form.cleaned_data['phone'],
                            special_instructions=form.cleaned_data.get('special_instructions', '')
                        )

                    # Create order
                    order = Order.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        shipping_address=shipping_address,
                        payment_provider=form.cleaned_data.get('payment_provider')
                    )

                    # Create order items + update stock
                    for cart_item in cart_items:
                        tree = (
                            Tree.objects
                            .select_for_update()
                            .get(id=cart_item['product'].id)
                        )

                        if tree.quantity < cart_item['quantity']:
                            raise ValueError(
                                f"Not enough stock for {tree.name}"
                            )

                        # decrease stock
                        tree.quantity -= cart_item['quantity']
                        tree.save()

                        OrderItem.objects.create(
                            order=order,
                            product=tree,
                            quantity=cart_item['quantity']
                        )

                    # Clear cart
                    cart.clear()

                    return redirect('users:home')

            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart:cart_summary')

    else:
        form = OrderPlacementForm(
            user=request.user if request.user.is_authenticated else None
        )

    return render(request, 'orders/order_placement_form.html', {
        'form': form,
        'is_authenticated': request.user.is_authenticated
    })

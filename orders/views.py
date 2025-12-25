from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ShippingAddressForm

# Create your views here.

@login_required
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
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from orders.models import ShippingAddress, Order

# Create your views here.

@login_required
def home(request):
    addresses = request.user.addresses.all()
    orders = request.user.orders.all()
    context = {
        'addresses': addresses,
        'orders': orders
    }
    return render(request, 'users/home.html', context)


# need to define sign_up view as it is not in 'django.contrib.auth.urls'
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})

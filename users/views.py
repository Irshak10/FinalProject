from django.shortcuts import render, redirect

from users.forms import CreateUserForm, CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.decorators import unauthenticated_user, allower_users
from django.contrib.auth.models import Group
from users.models import Customer
from testing.templates import *


@unauthenticated_user
def registration_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('index')

    context = {'form': form}
    return render(request, 'users/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'users/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allower_users(allowed_roles=['customer', 'admin'])
def user_page(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'users/user.html', context)

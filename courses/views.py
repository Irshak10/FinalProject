from django.shortcuts import render, redirect

from courses.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from courses.decorators import unauthenticated_user, allower_users, admin_only
from django.contrib.auth.models import Group
from courses.models import Customer


# Create your views here.


@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, 'courses/home.html')


@login_required(login_url='login')
@allower_users(allowed_roles=['customer'])
def course(request):
    return render(request, 'courses/course.html')


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

            return redirect('login')

    context = {'form': form}
    return render(request, 'courses/register.html', context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'courses/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allower_users(allowed_roles=['customer'])
def user_page(request):

    context = {}
    return render(request, 'courses/user.html', context)

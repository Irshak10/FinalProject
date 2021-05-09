from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.decorators import unauthenticated_user, allowed_mails
from users.models import Profile
from testing.models import UserProgress


@unauthenticated_user
def registration_page(request):
    """
    This function performs registration of a new user account.
    :return:
    If the verification is successful, the user's data is saved to the database.
    After which it is redirected to the login page, where he can log in using the current data of the new user.
    """
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            Profile.objects.get_or_create(
                user=user,
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'users/register.html', context)


@unauthenticated_user
def login_page(request):
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/topics/auth/default/#auth-web-requests

    This function is needed to check when the user logs in.
    Verification is carried out using the methods:
        authenticate(login and password verification) and login(opening access).
    """
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
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/topics/auth/default/#auth-web-requests
    To log out a user who has been logged in via django.contrib.auth.login(),
        use django.contrib.auth.logout() within your view.
    It takes an HttpRequest object and has no return value.
    :return: the user redirected to the Login page.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_mails()
def profile(request):
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/topics/auth/default/#auth-web-requests

    This function is responsible for displaying and changing all the profile data allowed for editing.
    Here you save the changed data, as well as display them after saving,
        by redirecting the user to your personal account with up-to-date data.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, f'Please correct the error below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    user_progress, created = UserProgress.objects.get_or_create(user=request.user)

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_info': user_progress,
    })


def password_reset_request(request):
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/topics/auth/default/

    Function for operation of password reset.
    Here you can specify the necessary settings for sending a letter with further instructions on how to reset your password.
    """
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Запрос на сброс пароля"
                    email_template_name = "users/password_reset_mail.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        # 'domain': 'corporate-portal.herokuapp.com',
                        'site_name': 'Corporate Portal',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'На ваш почтовый ящик отправлено сообщение с инструкциями по сбросу '
                                              'пароля')
                    return redirect("password_reset_done")
            messages.error(request, 'Введен неверный адрес электронной почты')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="users/password_reset.html",
                  context={"password_reset_form": password_reset_form})

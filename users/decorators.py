from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

from users.models import ConfirmedMail


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_mails():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            mails = []
            for i in ConfirmedMail.objects.all():
                mails.append(i.mails_list)
            if request.user.email in mails or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                User.objects.get(email=request.user.email).delete()
                return HttpResponse('Your mail is not confirmed by admin to view this page')
        return wrapper_func
    return decorator

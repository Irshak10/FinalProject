from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

from users.models import ConfirmedMail


def unauthenticated_user(view_func):
    """ Used as a decorator.
    Materials used:
    - https://docs.djangoproject.com/en/dev/topics/http/decorators/

    The unauthenticated_user function is used to check if the user is logged in.
    :return: If the user is already logged in, they are redirected to the Main page (Index).
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_mails():
    """ Used as a decorator.
    Materials used:
    - https://docs.djangoproject.com/en/dev/topics/http/decorators/

    The allowed_mails function checks if the user's mail (the user who is logging in) is in the list of objects.
    Also, access will be provided if the user is a superuser (admin)
    :return:
     - If there is a mail in the list, it gives access to the site pages (which are marked with this decorator).
        Also, access will be provided if the user is a superuser (admin).
        And user are redirected to the Main page (Index).
    - If the user's email is not in the list, a corresponding error will appear,
        and after that the user will be deleted from the database (with all data).
    """
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

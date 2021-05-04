from django.contrib import admin
from users.models import Profile, ConfirmedMail

# Register your models here.

admin.site.register(Profile)
admin.site.register(ConfirmedMail)

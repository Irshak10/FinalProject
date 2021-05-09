from django.contrib import admin

from users.models import Profile, ConfirmedMail


# Represents Profile and ConfirmedMail models at admin site.

admin.site.register(Profile)
admin.site.register(ConfirmedMail)

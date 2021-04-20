from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="static/images", default="static/images/default.png")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

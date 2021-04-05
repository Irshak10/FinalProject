from django.db import models
from django.contrib.auth.models import User


POSITION_CHOICES = [
    ('worker', 'Worker'),
    ('admin', 'Admin'),
    ('Chief', 'Chief')
    ]


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_picture = models.ImageField(
        upload_to="users/static/images",
        default="users/static/images/default.png",
        null=True,
        blank=True
    )
    position = models.CharField(max_length=15, default=None, choices=POSITION_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return 'Name: {0}, Phone: {1}, Email: {2}'.format(self.name, self.phone, self.email)


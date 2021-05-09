from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    The Profile model that is used in the user's personal account.
    Model has 4 attributes and 2 methods.
    Attributes:
        - user - used as a nickname for each user, has a binding of OneToOneField, to the Class User from the Auth model;
        - profile_picture - used as a profile photo, assigned only to this site.
            (initially installed by default also, the user can change his photo in his personal account);
        - phone_number - field for entering the user's phone number
            (Using PositiveIntegerField to input only positive numbers);
        - accept_email - this parameter is responsible for the ability to disable/enable sending messages to your mail.
    Methods:
        - __str__ - a standard method that is responsible for displaying information.
            The method expects only an instance as an argument and must return a string;
        - save - method used to save data to a profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='static/images', default='static/images/default.png')
    phone_number = models.PositiveIntegerField(default=0)
    accept_email = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ConfirmedMail(models.Model):
    """
    The ConfirmedMail model is designed to check if a user is on the list of allowed mails.
    The admin has the ability to enter authorized emails through the admin panel beforehand.
    Model has 1 attribute and 1 method.
    Attribute:
        - mails_list - field of type charField, which is used to indicate the allowed mail.
        The addition is made only by the Administrator
    Method:
        - __str__ - a standard method that is responsible for displaying information.
    """
    mails_list = models.CharField(max_length=30)

    def __str__(self):
        return self.mails_list


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/ref/signals/

    @receiver - the function to be bound to signal (used as a decorator);
    :param sender: Indicates a specific sender - User;
    :param instance: user=instance
    :param created: Checking and creating a user profile.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/ref/signals/

    @receiver - the function to be bound to signal (used as a decorator).
    :param sender: Indicates a specific sender - User;
    :param instance: instance.profile.save
    """
    instance.profile.save()



from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from users.models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Materials used:
    - https://docs.djangoproject.com/en/3.2/topics/auth/

    UserRegisterForm it`s form accepts the required parameters when registering a user.
    This User model is extended by the Profile model in models.py.
    This form also has an additional "clean_email" method that checks the uniqueness of the entered email.
    If the mail has already been registered earlier, an error will be generated.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Эта почта уже зарегистрирована')
        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    """
    UserUpdateForm is a form that is used to update user data in a personal account.
    Only two attributes can be changed in our form: first name, last name.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """
    ProfileUpdateForm is a form that is used to update user data (Profile model) in the personal account.
    You can change all the attributes of the Profile model.
    """
    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number', 'accept_email']

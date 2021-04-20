from django.urls import path, include
from django.views.generic import TemplateView
from users.views import registration_page, login_page, logout_page, profile


urlpatterns = [
    path('test/', TemplateView.as_view(template_name='users/login.html')),
    path('accounts/', include('allauth.urls')),
    path('login/', login_page, name='login'),
    path('register/', registration_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile, name='profile'),
]

from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from users.views import registration_page, login_page, logout_page, profile


urlpatterns = [
    path('test/', TemplateView.as_view(template_name='users/login.html')),
    path('accounts/', include('allauth.urls')),
    path('login/', login_page, name='login'),
    path('register/', registration_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile, name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),  name='password_reset_confirm'),
    path('password-reset-complate', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),  name='password_reset_complete')

]

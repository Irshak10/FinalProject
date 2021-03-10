"""FinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from courses.views import home, course, registration_page, login_page, logout_page


urlpatterns = [
    path('test/', TemplateView.as_view(template_name='courses/login.html')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login/', login_page, name='login'),

    path('register/', registration_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('', home, name='home'),
    path('course/', course, name='course'),
]
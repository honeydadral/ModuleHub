"""
URL configuration for itapps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, n
        2. Add a URL to urlpatterns:  path('', views.home, name='home')ame='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from users import views as user_views
# from users import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='core-home'),
    path('about/', views.about, name='core-about'),
    path('register/', user_views.register, name='register'),
    path('contact/', views.contact_view, name='core-contact'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
]

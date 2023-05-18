from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "accounts"

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', login_required(views.logout_user), name='logout'),
    path('signup_user', views.signup_user, name='signup_user')
]
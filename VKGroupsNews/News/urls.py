from django.urls import path
from .views import hook, parse_group
from rest_framework.authtoken import views as auth_views

app_name = "News"

urlpatterns = [
    path("vk_hook", hook),
    path("parse", parse_group),
    path(r'auth/', auth_views.obtain_auth_token)
]
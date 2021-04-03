from django.urls import path
from .views import test

app_name = "News"

urlpatterns = [
    path("",test)
]
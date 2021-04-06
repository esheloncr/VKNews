from django.urls import path
from .views import parse, ArticleApiView, hook

app_name = "News"

urlpatterns = [
    path("parse", parse),
    path("api/Article", ArticleApiView.as_view()),
    path("vk_hook", hook)
]
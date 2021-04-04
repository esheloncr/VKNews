from django.urls import path
from .views import parse, ArticleApiView, respond

app_name = "News"

urlpatterns = [
    path("parse", parse),
    path("api/Article", ArticleApiView.as_view()),
    path("new_post",respond)
]
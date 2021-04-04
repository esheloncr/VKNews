from django.urls import path
from .views import parse, ArticleApiView

app_name = "News"

urlpatterns = [
    path("parse", parse),
    path("api/Article", ArticleApiView.as_view())
]
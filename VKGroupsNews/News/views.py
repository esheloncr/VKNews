import json
from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from .models import Article
from .serializers import ArticleSerializer
from .vkparser import get_post_by_hook, parse_posts


@csrf_exempt
def hook(request):
    if request.method == "GET":
        return redirect("/")
    event = json.loads(request.body.decode("utf-8"))
    if event["type"] == "wall_post_new":
        get_post_by_hook(event)
        return HttpResponse("ok")


class ArticleAPIView(ListModelMixin, GenericViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = [
        'local_post_link',
    ]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if "order_by_date" in self.request.query_params:
            return Article.objects.all().order_by("date_published")
        return Article.objects.all()


def parse_group(request):
    parse_posts()
    return HttpResponse("Готово")


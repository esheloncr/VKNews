from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from .VkParser import get_info
from .forms import TestForm


def parse(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data.get("login")
            password = form.cleaned_data.get("password")
            group_id = "-" + str(form.cleaned_data.get("group_id"))
            get_info(group_id, login, password)
            return HttpResponse("Успешно")
    else:
        form = TestForm()
    return render(request, "login.html", context={"form":form})


def respond(request):
    # webhook body
    return redirect("/parse")


class ArticleApiView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        filters = request.GET.get("filter_by", None)
        local_post_id = request.GET.get("id", None)
        if local_post_id:
            articles = Article.objects.all().filter(local_post_link__contains=local_post_id)
            serializer = ArticleSerializer(articles, many=True)
            return Response({"Articles": serializer.data})
        elif filters == "date":
            articles = Article.objects.all().order_by("-date_published")
            paginator_articles = Paginator(articles, 10)
            page_number = request.GET.get("page")
            if page_number is None:
                page_number = 1
            paginated_articles = paginator_articles.get_page(page_number)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return Response({"articles": serializer.data})
        elif filters == "reverse_date":
            articles = Article.objects.all().order_by("date_published")
            paginator_articles = Paginator(articles, 10)
            page_number = request.GET.get("page")
            if page_number is None:
                page_number = 1
            paginated_articles = paginator_articles.get_page(page_number)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return Response({"articles": serializer.data})
        else:
            paginator_articles = Paginator(articles, 10)
            page_number = request.GET.get("page")
            if page_number is None:
                page_number = 1
            paginated_articles = paginator_articles.get_page(page_number)
            serializer = ArticleSerializer(paginated_articles, many=True)
            return Response({"Articles": serializer.data})

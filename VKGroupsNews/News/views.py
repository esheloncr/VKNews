from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article
from .serializers import ArticleSerializer
from .VkParser import get_info
from django import forms
# Create your views here.


class TestForm(forms.Form):
    login = forms.CharField(label="Логин", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    group_id = forms.IntegerField()


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


class ArticleApiView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        local_post_id = request.GET.get("local_post_link", None)
        if local_post_id:
            articles = Article.objects.all().filter(local_post_link__contains=local_post_id)
            serializer = ArticleSerializer(articles, many=True)
            return Response({"articles": serializer.data})
        else:
            serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})
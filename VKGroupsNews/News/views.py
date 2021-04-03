from django.shortcuts import render, redirect, HttpResponse
from .VkParser import get_info
# Create your views here.


def test(request):
    asdasd = -201788787
    get_info(asdasd,1)
    return HttpResponse()
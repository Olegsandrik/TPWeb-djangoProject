from django.shortcuts import render
from django.http import HttpResponse, Http404


def ask(request):
    return render(request, "app/ask.html")


def base(request):
    return render(request, "app/index.html")


def login(request):
    return render(request, "app/login.html")


def singup(request):
    return render(request, "app/singup.html")


def hot(request):
    return render(request,"app/hot.html")


def tag(request, tagname):
    return render(request,"app/tag.html", {'tagname': tagname})


def question(request, number):
    return render(request, "app/question.html",{'number': number})


def paginate(objects_list, request, per_page=10):
    # do smth with Paginator, etc…
    return Http404
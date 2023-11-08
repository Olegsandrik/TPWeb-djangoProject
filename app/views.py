from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator


def ask(request):
    return render(request, "app/ask.html")


questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'Long lorem ipsum {i}',
            'answers': i*2+3,
            'tags': 'example',
        } for i in range(10)
    ]


def hot(request):
    set_page = {'1', '2', '3', '4'}
    page = request.GET.get("page", 1)
    if page in set_page:
        return render(request, "app/hot.html", {'questions': paginate(questions, page, 3)})
    return render(request, "app/hot.html", {'questions': paginate(questions, 1, 3)})


def home(request):
    set_page = {'1', '2', '3', '4'}
    page = request.GET.get("page", 1)
    if page in set_page:
        return render(request, "app/home.html", {'questions': paginate(questions, page, 3)})
    return render(request, "app/home.html", {'questions': paginate(questions, 1, 3)})


def login(request):
    return render(request, "app/login.html")


def singup(request):
    return render(request, "app/singup.html")




def tag(request, tagname):
    return render(request, "app/tag.html", {'tagname': tagname})


def question(request, number):
    item = questions[number]
    return render(request, "app/question.html", {'question': item})


def paginate(objects_list, page, per_page=10):
    paginator = Paginator(objects_list, per_page)
    return paginator.page(page)
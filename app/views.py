from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from app.forms import LoginForm, RegisterForm
from app.models import Profile, Question, Answer





def ask(request):
    return render(request, "app/ask.html")


def index(request):
    questionsnew = Question.objects.get_new_questions()
    set_page = []
    for i in range(1, min(len(questionsnew), 6), 1):
        set_page.append(f"{i}")
    if len(questionsnew)==1:
        set_page = ['1']
    page = request.GET.get("page", '1')
    if page in set_page:
        return render(request, "app/test.html", {'questions': paginate(questionsnew, page, 3),
                                                'pages': set_page})
    raise Http404('Страница не найдена')


def hot(request):
    questionshot = Question.objects.get_hot_questions()
    set_page = []
    for i in range(1, min(len(questionshot), 6), 1):
        set_page.append(f"{i}")
    if len(questionshot) == 1:
            set_page = ['1']
    page = request.GET.get("page", '1')
    if page in set_page:
        return render(request, "app/hot.html", {'questions': paginate(questionshot, page, 3),
                                                 'pages': set_page})
    raise Http404('Страница не найдена')


@login_required(redirect_field_name='continue')
def home(request):
    questionsnew = Question.objects.get_new_questions()
    set_page = []
    for i in range(1, min(len(questionsnew), 4), 1):
        set_page.append(f"{i}")
    if len(questionsnew)==1:
        set_page = ['1']
    page = request.GET.get("page", '1')
    if page in set_page:
        return render(request, "app/home.html", {'questions': paginate(questionsnew, page, 3),
                                                 'pages': set_page})
    raise Http404('Страница не найдена')

@csrf_protect
def mylogin(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            #print(user)
            if user is not None:
                login(request, user)
                #print("sucsess")
                return redirect(reverse('home')) # request.Get.get('continue', '/') или revers('home')
            else:
                login_form.add_error(None, "Wrong password or user does not exist.")
    return render(request, "app/login.html", context={'form': login_form})


@csrf_protect
def singup(request):
    if request.method == 'GET':
        registr_form = RegisterForm()
    if request.method == 'POST':
        registr_form = RegisterForm(request.POST)
        if registr_form.is_valid():
            user = registr_form.save()
            if user:
                print("sucsessfully registered")
                return redirect(reverse('home')) # request.Get.get('continue', '/') или revers('home')
            else:
                registr_form.add_error(None, "User saving error!")
    return render(request, "app/singup.html", context={'form': registr_form})


def tag(request, tagname):
    questionstag = Question.objects.get_questions_with_tag(tagname)
    set_page = []
    for i in range(1, min(len(questionstag), 6), 1):
        set_page.append(f"{i}")
    if len(questionstag)==1:
        set_page = ['1']
    page = request.GET.get("page", '1')
    if page in set_page:
        return render(request, "app/test.html", {'questions': paginate(questionstag, page, 3),
                                                 'pages': set_page, 'tagname': tagname})
    raise Http404('Страница не найдена')

def question(request, number):
    questionsreal = Question.objects.all()
    set_page = []
    for i in range(1, min(len(questionsreal), 4), 1):
        set_page.append(f"{i}")
    page = request.GET.get("page", '1')
    item = questionsreal[number-1]
    if page in set_page:
        return render(request, "app/question.html", {'question': item,
                                                     'pages': set_page})
    raise Http404('Страница не найдена')


def paginate(objects_list, page, per_page=10):
    paginator = Paginator(objects_list, per_page)
    return paginator.page(page)
from django.urls import path
from . import views
urlpatterns = [
    path('', views.base, name='home'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('singup/', views.singup, name='singup'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tagname>/', views.tag, name='tag'),
    path('question/<int:number>/', views.question, name='question'),
]

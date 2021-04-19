from django.urls import path
from . import views

app_name = 'play'
urlpatterns = [
    path('play/', views.index, name='index'),
    path('play/answer/', views.answer, name='answer'),
    path('play/test/', views.test, name='test')

]

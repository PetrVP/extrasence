from django.urls import path
from . import views

app_name = 'play'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('answer/', views.Answer.as_view(), name='answer'),

]

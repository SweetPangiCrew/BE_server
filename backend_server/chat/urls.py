# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("send/<str:game_name>", views.send, name="send"),
     path("list/<str:game_name>", views.chat_list, name="list"),
]

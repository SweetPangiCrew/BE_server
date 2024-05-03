from django.urls import path
from . import views

from .views import *

urlpatterns = [
 
   path('registration/', CreateUserView.as_view(), name='registration'),
   path('create-game-stage/', CreateGameStageView.as_view(), name='create-game-stage'),
]
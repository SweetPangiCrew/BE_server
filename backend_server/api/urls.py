from django.urls import path
from . import views

urlpatterns = [
    path('npc/movement/<str:sim_code>/<int:step>/', views.movement,name="get_reaction"),
    path('npc/perceive/<str:sim_code>/<int:step>/', views.perceive,name="post_perceive"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('npc/movement/<str:sim_code>/<int:step>/<str:user>', views.movement,name="get_reaction"),
    path('npc/perceive/<str:sim_code>/<int:step>/<str:user>', views.perceive,name="post_perceive"),
    path('npc/loadReligiousIndex/<str:game_name>/<str:user>', views.loadReligiousIndex,name="get_relgious"),
    path('npc/updateReligiousIndex/<str:game_name>/<str:user>', views.updateReligiousIndex,name="put_relgious"),
    path('servertime/', views.servertime,name="get_servertime"),
    path('existingGames/<str:user>', views.loadgames,name="get_games"),
#    path('gamestart/', views.gamestart,name="game_start"),
  
]
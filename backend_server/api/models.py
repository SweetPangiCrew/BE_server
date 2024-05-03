from django.db import models
from django.contrib.auth.models import User

class GameStage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=10)
    sim_code = models.CharField(max_length=50, default='agenti_15')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user.username} - Game {self.gm}"
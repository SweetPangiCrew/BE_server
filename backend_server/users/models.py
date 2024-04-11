
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid



class MyUserManager(BaseUserManager):
    def create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        user.save(using=self._db)
        user.set_password('1') 
        return user

class MyUser(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 필요한 추가 필드

    objects = MyUserManager()
    #username = 
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return str(self.username)
    

class GameStage(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=10,unique=True)
    sim_code = models.CharField(max_length=50, default='agenti_15')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user.username} - Game {self.game_name}"
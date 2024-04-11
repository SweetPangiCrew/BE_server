from rest_framework import serializers
from .models import *

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['uuid', 'username']  # username 필드를 포함시킵니다.
        read_only_fields = ('uuid',)  


class GameStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameStage
        fields = ['id', 'user', 'game_name', 'sim_code', 'is_completed', 'created_at']
        read_only_fields = ('id', 'created_at')  # 자동 생성되는 필드는 읽기 전용으로 설정
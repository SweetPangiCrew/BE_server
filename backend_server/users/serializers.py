from rest_framework import serializers
from .models import *
from users.models import MyUser

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


class UserUUIDSerializer(serializers.Serializer):
    user = serializers.CharField()

    # def validate_user(self, value):
    #     try:
    #         return MyUser.objects.get(uuid=value)
    #     except MyUser.DoesNotExist:
    #         raise serializers.ValidationError("No user with this UUID exists.")
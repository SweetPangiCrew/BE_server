from rest_framework import serializers

class MovementFileSerializer(serializers.Serializer):
    movement_file = serializers.FileField()

class religiousSerializer(serializers.Serializer):
    persona = serializers.CharField()
    deltaValue = serializers.CharField()

class testSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    
class perceivedTileSerializer(serializers.Serializer):
    dist = serializers.CharField()
    event = serializers.ListField(child=serializers.CharField(allow_null=True))

class perceivePerPersonaSerializer(serializers.Serializer):
    persona = serializers.CharField()
    curr_address = serializers.CharField()
    perceived_tiles = perceivedTileSerializer(many=True)
  

class UserUUIDSerializer(serializers.Serializer):
    user = serializers.CharField()

class CurrTimeSerializer(serializers.Serializer):
    curr_time = serializers.DateTimeField(format='%B %d, %Y, %H:%M:%S')

class perceiveSerializer(serializers.Serializer):
    perceived_info = perceivePerPersonaSerializer(many=True)
    meta = CurrTimeSerializer()


class gamestartSerializer(serializers.Serializer):
    sim_code = serializers.CharField()
    game_name = serializers.CharField()



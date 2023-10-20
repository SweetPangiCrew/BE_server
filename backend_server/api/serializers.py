from rest_framework import serializers

class MovementFileSerializer(serializers.Serializer):
    movement_file = serializers.FileField()


class testSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    
class perceivedTileSerializer(serializers.Serializer):
    dist = serializers.CharField()
    event = serializers.ListField(child=serializers.CharField(allow_null=True))

#class eventSerializer(serializers.Serializer):


class perceiveSerializer(serializers.Serializer):
    curr_address = serializers.CharField()
    perceived_tiles = perceivedTileSerializer(many=True)


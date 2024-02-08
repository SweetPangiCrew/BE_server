from rest_framework import serializers



class sendSerializer(serializers.Serializer):
    persona = serializers.CharField()
    message = serializers.CharField()
    round = serializers.CharField()
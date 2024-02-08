
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect
from rest_framework import status

#from ..persona.cognitive_modules.converse import agent_with_user_chat
import os, json, datetime, pickle

from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes

from rest_framework.request import Request
from rest_framework.response import Response
import io
from rest_framework.parsers import JSONParser

from .serializers import *

is_ubuntu_server = False
if os.path.exists('/etc/os-release'):
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if line.startswith('ID=ubuntu'):
                is_ubuntu_server = True
                break

# 변수 설정
if is_ubuntu_server:
    fs_storage = "/home/ubuntu/BE_server/backend_server/storage"
    game_storage = "/home/ubuntu/BE_server/backend_server/games"
else:
    fs_storage = "./storage"
    game_storage = "./games"


def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@api_view(['POST'])
def send(request, game_name):

    # message를 chat gpt api 를 호출하고.. 음 그리고 받기.. 흑 
        stream = io.BytesIO(request.body)
        #stream = stream.replace("'", "\"") 
        data = JSONParser().parse(stream) #stream data 가 Dict가 됨.
        #print(stream)
      
        print(data)
        serializer = sendSerializer(data=data)
        if(serializer.is_valid()):
            persona = serializer.validated_data["persona"]
            message = serializer.validated_data["message"]
            round = serializer.validated_data["round"]
            
        else: 
             print("serialize 실패") 
             meta = { "meta": { "code": 404, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
             return  Response(data=meta,status= status.HTTP_400_BAD_REQUEST)
        
        #try:
        rs_file = f"{game_storage}/{game_name}.pkl"
        with open(rs_file, 'rb') as file:
                    gameInstance = pickle.load(file)
                    re_message, end = gameInstance.user_chat(persona,message,round)

                    data = {"meta": { "code": 0, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
                    data["response"] = re_message
                    data["round"] = round
                    data["end"] =  end

                    with open(rs_file, 'wb') as file:
                        pickle.dump(gameInstance, file)
                    return Response(data=data, status= status.HTTP_200_OK)
        
        
        
        
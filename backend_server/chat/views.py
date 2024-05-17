
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

from users.serializers import *


fs_storage = "./storage"
game_storage = "./pickles"

@api_view(['GET'])
def chat_list(request, game_name,user):
    userID = MyUser.objects.get(uuid=user)

    sim_folder = f"{fs_storage}/{userID}/{game_name}"
    user_file = f"{sim_folder}/reverie/user.json"
    
    data = dict()
    data['meta'] = dict()

    #유저 네임 테스트 코드
    with open(f"{sim_folder}/reverie/user.json", encoding = 'UTF8') as json_file:  
      reverie_user = json.load(json_file)

    with open(f"{sim_folder}/reverie/user.json", "w", encoding = 'UTF8') as outfile: 
      reverie_user["username"] = userID.username
      outfile.write(json.dumps(reverie_user, indent=2, ensure_ascii = False))
    ## 삭제 가능  
    
    try:
        with open(user_file, encoding = 'UTF8') as json_file:  
            reverie_user = json.load(json_file)
            data["chat_list"] = reverie_user["chat_list"]
            data['meta']['code'] = 0

    except: 
           
           data['meta']['code'] = 404
    
    return Response(data)



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
            user = serializer.validated_data["uuid"]
            userID = MyUser.objects.get(uuid=user)
         
        else: 
             print("serialize 실패") 
             meta = { "meta": { "code": 404, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
             return  Response(data=meta,status= status.HTTP_400_BAD_REQUEST)
        
        rs_file = f"{game_storage}/{userID}/{game_name}.pkl" 

        with open(rs_file, 'rb') as file:
                    gameInstance = pickle.load(file)
                    re_message, end = gameInstance.user_chat(persona,message,round)
                    
                    data = {"meta": { "code": 0, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
                    data["body"] = dict()
                    data["body"]["response"] = re_message
                    data["body"]["round"] = round
                    data["body"]["end"] =  end

                    with open(rs_file, 'wb') as file:
                        pickle.dump(gameInstance, file)
                    return Response(data=data, status= status.HTTP_200_OK)
        
        
        
        
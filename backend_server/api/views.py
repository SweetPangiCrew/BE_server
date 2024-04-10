#
from global_methods import *
from reverie import *
from .serializers import perceiveSerializer,gamestartSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status
from rest_framework.decorators import APIView, api_view, permission_classes

from rest_framework.request import Request
from rest_framework.response import Response
import io
from rest_framework.parsers import JSONParser
import datetime
import sys
import pickle
#from utils import *
import json
import os



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



@api_view(['GET'])
def loadReligiousIndex(request,game_name):

        rs_file = f"{game_storage}/{game_name}.pkl"

        with open(rs_file, 'rb') as file:
                    gameInstance = pickle.load(file)

                    data = {"religious_index": dict(), 
                       "meta": dict()}
          
                    #페르소나 하나씩 순회
                    for persona_name, persona in gameInstance.personas.items():  
                        
                        #movements["religious_index"][persona_name] = {}
                        data["religious_index"][persona_name] = persona.scratch.religious_index
            
                                
                    data["meta"] = { "code": 0, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }
                    
                    return Response(data=data, status= status.HTTP_200_OK)
        
    

@api_view(['PUT'])
def updateReligiousIndex(request,game_name):


        stream = io.BytesIO(request.body)
        #stream = stream.replace("'", "\"") 
        data = JSONParser().parse(stream) #stream data 가 Dict가 됨.
        #print(stream)
      
        print(data)
        #parsed_data = json.loads(data)
        # serializer = (data=data)
        # if(serializer.is_valid()):
        #     persona = serializer.validated_data["persona"]
        #     message = serializer.validated_data["message"]
        #     round = serializer.validated_data["round"]
            
        # else: 
        #      print("serialize 실패") 
        #      meta = { "meta": { "code": 404, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
        #      return  Response(data=meta,status= status.HTTP_400_BAD_REQUEST)
        
        rs_file = f"{game_storage}/{game_name}.pkl"

        with open(rs_file, 'rb') as file:
                    gameInstance = pickle.load(file)

                    gameInstance.update_religious_index(data["update_religious_index"])

                    updated_data = {"religious_index": dict(), 
                       "meta": dict()}
                    
                    for persona_name in data["update_religious_index"].keys() :  
                    
                        updated_data["religious_index"][persona_name] = gameInstance.personas[persona_name].scratch.religious_index
                                
                    updated_data["meta"] = { "code": 0, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }
                    
                    return Response(data=updated_data, status= status.HTTP_200_OK)
    

@api_view(['GET'])
def servertime(request):

    data = {"serverTime": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }
     
    return Response(data)


@api_view(['GET'])
def movement(request,sim_code,step):

    try: 
        sim_folder = f"{fs_storage}/{sim_code}"
        curr_move_file = f"{sim_folder}/movement/{step}.json"
        #absolute_path = os.path.abspath(curr_move_file)
        #print(absolute_path)
        with open(curr_move_file, encoding = 'UTF8') as json_file:
            data = json.load(json_file)
            data['meta']['code'] = 0
    except: 
           data = {"There's no json file"+ sim_folder+"/"+ str(step) } 
           data['meta']['code'] = 404
    
    return Response(data)




@api_view(['POST'])
def perceive(request,sim_code,step):
     
        stream = io.BytesIO(request.body)
        #stream = stream.replace("'", "\"") 
        data = JSONParser().parse(stream) #stream data 가 Dict가 됨.
        #print(stream)
      
        print(data)
        serializer = perceiveSerializer(data=data)
        curr_time_d = ""
        if(serializer.is_valid()):
            curr_time_d = serializer.validated_data["meta"]["curr_time"]
            pass
            #print(serializer.validated_data)
        else: 
             print("serialize 실패") 
             data['meta']['code'] = 400
             return  Response(data=data,status= status.HTTP_400_BAD_REQUEST)

        try: 
            sim_folder = f"{fs_storage}/{sim_code}"
            curr_perceive_file = f"{sim_folder}/perceive/{step}.json"

            os.makedirs(os.path.dirname(curr_perceive_file), exist_ok=True)
           
            serializer.validated_data["meta"]["curr_time"]= serializer.validated_data["meta"]["curr_time"].strftime("%B %d, %Y, %H:%M:%S")
            with open(curr_perceive_file, "w", encoding = 'UTF8') as outfile: 
                outfile.write((json.dumps(serializer.validated_data, indent=2, ensure_ascii = False))) 

        
        except Exception as e:
            print(f"perceive 저장 실패: {e}")
            meta = { "meta": { "code": 401, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
            return Response(data=meta,status= status.HTTP_400_BAD_REQUEST)
        
        
        #try:
        rs_file = f"{game_storage}/{sim_code}.pkl"
        with open(rs_file, 'rb') as file:
                    gameInstance = pickle.load(file)
                    gameInstance.step = step
                    gameInstance.curr_time = curr_time_d
             
                    gameInstance.start_server(1)
                    print("game_curr_time ~~~~~~~~~~~~~~~~~~~~"+str(gameInstance.curr_time))
                    print("game ~~~~~~~~~~~~~~~~~~~~"+str(gameInstance))

                    gameInstance.save()
                    # with open(rs_file, 'wb') as file:
                    #     pickle.dump( gameInstance, file)
                    
                    meta = { "meta": { "code": 0, "date": gameInstance.curr_time.strftime("%B %d, %Y, %H:%M:%S") }}
                    return Response(data=meta,status= status.HTTP_201_CREATED)
            

        # except :
        #      print("해당 게임 인스턴스가 존재하지 않습니다.")
        #      meta = { "meta": { "code": 401, "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
        #      return Response(data=meta,status= status.HTTP_201_CREATED)



@api_view(['POST'])
def gamestart(request):
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        serializer = gamestartSerializer(data=data)
        if(serializer.is_valid()):
           print(serializer.validated_data)
        else: 
             print("serialize 실패") 
             data['meta']['code'] = 400
             return  Response(data=data,status= status.HTTP_400_BAD_REQUEST)
        
        simcode = serializer.validated_data["sim_code"]
        gamename = serializer.validated_data["game_name"]

        try:
            
            rs = ReverieServer(simcode, gamename)

            rs_file = f"{game_storage}/{gamename}.pkl"
            with open(rs_file, 'wb') as file:
                pickle.dump( rs, file)
            rs.start_server(1) #base에 있는 Perceive 0으로 1번 인지추론 과정을 거쳐서 첫번째 Getmovement를 생성
            #print(rs[gamename])
            meta = { "meta": { "code": 0,"opened game": gamename ,"date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}
            return Response(data=meta,status= status.HTTP_201_CREATED)
        
        except:
            meta["code"] = 1
            meta["openedgame"] = "전역 변수 인스턴스에 다른 값이 이미 존재함."
            return Response(data=meta,status= status.HTTP_400_BAD_REQUEST)
            
        
@api_view(['GET'])
def loadgames(request):

    try: 
        # 해당 폴더에 있는 파일 목록을 얻기
        file_list = os.listdir(game_storage)
        data= dict()
        data["games"] = dict()
        # 파일 목록 출력
        for file_name in file_list:
               
            game_name, game_extension = os.path.splitext(os.path.basename(file_name))

            
            curr_move_file = f"{fs_storage}/{game_name}/reverie/meta.json"

            with open(curr_move_file, encoding = 'UTF8') as json_file:
                data["games"][game_name] =json.load(json_file)

       
        data['meta'] = dict()
        data['meta']['code'] = 0

        print(data)
            
    except: 
           data = {"There's no json file"+ curr_move_file+"/" } 
           data['meta']['code'] = 404
    
    return Response(data)


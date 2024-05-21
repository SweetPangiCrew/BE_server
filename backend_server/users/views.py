from django.shortcuts import render
from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import MyUser
from .serializers import *

from global_methods import *
from reverie import *
import datetime
import pickle


#legacy
def getTestUser():

    user, created = MyUser.objects.get_or_create(
            uuid="9a727eb7-6437-4d03-a438-d09eb273f930",
            defaults={'username': 'TestUser'})
    
    return user


class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 유효한 데이터인 경우, MyUser 객체를 생성합니다.
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateGameStageView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GameStageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()

                simcode = serializer.validated_data["sim_code"]
                gamename = serializer.validated_data["game_name"]
                userID = serializer.validated_data["user"]

                
                fs_storage = "./storage" 
                game_storage = "./pickles"
                
                game_storage = f"{game_storage}/{userID}"
                # 경로 확인 및 생성
                os.makedirs(game_storage, exist_ok=True)

                rs = ReverieServer(simcode, gamename,userID)
                rs.user = userID
                rs_file = os.path.join(game_storage, f"{gamename}.pkl")
                rs_file = f"{game_storage}/{gamename}.pkl"

                with open(rs_file, 'wb') as file:
                    pickle.dump(rs, file)

                #rs.start_server(1) #base에 있는 Perceive 0으로 1번 인지추론 과정을 거쳐서 첫번째 Getmovement를 생성
                #rs.save()
               
                meta = { "meta": { "code": 0,"opened game": gamename ,"date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") }}

                return Response(meta, status=status.HTTP_201_CREATED) 

             
              
            except FileExistsError as e:  # game_name이 이미 존재하는 경우
                data = {'error': '동일한 게임 이름이 존재합니다.'}

                print(e)
                print(data)
                return Response(data,
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                 print(e)
                 return Response({'error': '현재 서버 점검 중입니다. 개발자에게 문의하세요.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': '현재 서버 점검 중입니다. 개발자에게 문의하세요.'}, status=status.HTTP_400_BAD_REQUEST)
    


    

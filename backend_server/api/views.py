from .serializers import perceiveSerializer
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




#from utils import *
import json
import os

fs_storage = "./storage"

@api_view(['GET'])
def movement(request,sim_code,step):


    try: 
        sim_folder = f"{fs_storage}/{sim_code}"
        curr_move_file = f"{sim_folder}/movement/{step}.json"
        #absolute_path = os.path.abspath(curr_move_file)
        #print(absolute_path)
        with open(curr_move_file, encoding = 'UTF8') as json_file:
            data = json.load(json_file)
            
    except: 
           data = {"There's no json file"+ sim_folder+"/"+ str(step) } 
    
    return Response(data)

@api_view(['POST'])
def perceive(request,sim_code,step):

        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        print(data)
        serializer = perceiveSerializer(data=data)
        if(serializer.is_valid()):
           print(serializer.validated_data)
        else: 
             print("serialize 실패") 
             return  Response(data=request.body,status= status.HTTP_400_BAD_REQUEST)

    #try: 
        sim_folder = f"{fs_storage}/{sim_code}"
        curr_perceive_file = f"{sim_folder}/perceive/{step}.json"

        os.makedirs(os.path.dirname(curr_perceive_file), exist_ok=True)
        #request.body.decode('utf8')
        with open(curr_perceive_file, "w", encoding = 'UTF8') as outfile: 
            outfile.write((json.dumps(serializer.validated_data, indent=2, ensure_ascii = False))) #

        return Response(data="abc",status= status.HTTP_201_CREATED)
            
    # except: 
    #        pass
    
    

    



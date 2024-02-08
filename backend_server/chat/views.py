
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render,redirect
from rest_framework import status


def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

@api_view(['GET'])
def send(request):

    try: 
        pass
    except: 
           data = {"There's no json file"+ sim_folder+"/"+ str(step) } 
           data['meta']['code'] = 404
    
    return Response(data)
from rest_framework.test import APITestCase, APIRequestFactory
from .views import send
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import json
from rest_framework.renderers import JSONRenderer
import random

User = get_user_model()

class sendTestCase(APITestCase):

    def test_move(self):
        
        self.view = send

        #scratch에 로컬 저장이 안됨 -> 당연히 안됨. 인스턴스에 저장이 되나를 봐야함?!!!!!11
        sample_data = {"persona": "나주교", "message": "a","round": 3}

        self.url = reverse("send",None,["game1"])
        response = self.client.post(self.url, sample_data, format ='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class chatListTestCase(APITestCase):

    def test(self):
        response = self.client.get(reverse("list",None,["game1"]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

# class PostPerceiveTestCase(APITestCase):

#     def setUp(self):
#         #self.view= perceive
#         self.url=reverse("post_perceive",None,["test4","0"])

#     # def test_post(self):
#     #     response = self.client.get(self.url)

#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_post_creation(self):


#         sample_data = {"perceived_info" : [
# 			{   "persona": "Isabella Rodriguez",
# 					"curr_address" : "the Ville:Isabella Rodriguez's apartment:main room:bed",
# 					"perceived_tiles" : [
# 					      {
# 					          "dist" : 0.0,
# 					          "event" : ["the Ville:Isabella Rodriguez's apartment:main room:bed", "be", "used", "being used"]
# 					      },
# 					      {
# 					          "dist" : 0.0,
# 					          "event" : ["Isabella Rodriguez", "is", "sleeping", "sleeping"]
# 					      },
# 								{
# 					          "dist" : 1.0,
# 					          "event" : ["the Ville:Isabella Rodriguez's apartment:main room:bed", None, None, None]
# 					      }
# 					  ]
# 			},

# 	{"persona": "Klaus Mueller",
# 	 "curr_address" : "the Ville:Dorm for Oak Hill College:Klaus Mueller's room",
# 	"perceived_tiles" : []
# 	},

# 	{   "persona": "Maria Lopez",
# 					"curr_address" : "the Ville:Isabella Rodriguez's apartment:main room:bed",
# 					"perceived_tiles" : []
# 	}

# ]
# }

#         #sample_data = {"title": "Sample title", "content": "Sample content"}
#         #json.dump(sample_data)
#         #JSONRenderer().render(sample_data)
#         #print(sample_data)
#         response = self.client.post(self.url, sample_data, format ='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        

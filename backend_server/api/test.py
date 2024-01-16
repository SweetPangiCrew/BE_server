from rest_framework.test import APITestCase, APIRequestFactory
from .views import perceive
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
import json
from rest_framework.renderers import JSONRenderer
import random

User = get_user_model()

class MovementTestCase(APITestCase):

    def test_move(self):
        response = self.client.get(reverse("get_reaction",None,["test4","0"]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class PostPerceiveTestCase(APITestCase):

    def setUp(self):
        #self.view= perceive
        self.url=reverse("post_perceive",None,["test4","0"])

    # def test_post(self):
    #     response = self.client.get(self.url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_creation(self):


        sample_data = {"perceived_info" : [
			{   "persona": "Isabella Rodriguez",
					"curr_address" : "the Ville:Isabella Rodriguez's apartment:main room:bed",
					"perceived_tiles" : [
					      {
					          "dist" : 0.0,
					          "event" : ["the Ville:Isabella Rodriguez's apartment:main room:bed", "be", "used", "being used"]
					      },
					      {
					          "dist" : 0.0,
					          "event" : ["Isabella Rodriguez", "is", "sleeping", "sleeping"]
					      },
								{
					          "dist" : 1.0,
					          "event" : ["the Ville:Isabella Rodriguez's apartment:main room:bed", None, None, None]
					      }
					  ]
			},

	{"persona": "Klaus Mueller",
	 "curr_address" : "the Ville:Dorm for Oak Hill College:Klaus Mueller's room",
	"perceived_tiles" : []
	},

	{   "persona": "Maria Lopez",
					"curr_address" : "the Ville:Isabella Rodriguez's apartment:main room:bed",
					"perceived_tiles" : []
	}

]
}

        #sample_data = {"title": "Sample title", "content": "Sample content"}
        #json.dump(sample_data)
        #JSONRenderer().render(sample_data)
        #print(sample_data)
        response = self.client.post(self.url, sample_data, format ='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
       # serializedResponse = json.loads(response.data)
        #self.assertEqual(serializedResponse.data["title"], sample_data["title"])
        

class PostGameStartTestCase(APITestCase):

    def setUp(self):
        #self.view= perceive
        self.url=reverse("game_start",None)

    # def test_post(self):
    #     response = self.client.get(self.url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_creation(self):


        sample_data = {	
            "sim_code" : "agenti", #base -> assembly_attendance 에러가 남(base scratch는 수정 안됐으니까.) agenti -> 나주교 에러가남.
			"game_name": "gameTest01161" 
		}

        sample_data["game_name"] = "gameTestRandom"+str(random.randint(1, 100))

        #sample_data = {"title": "Sample title", "content": "Sample content"}
        #json.dump(sample_data)
        #JSONRenderer().render(sample_data)
        #print(sample_data)
        response = self.client.post(self.url, sample_data, format ='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)
       # serializedResponse = json.loads(response.data)
        #self.assertEqual(serializedResponse.data["title"], sample_data["title"])
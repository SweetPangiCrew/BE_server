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

    #이거 Setup 안해두면 어차피 에러남.
    def test_move(self):
        
        response = self.client.get(reverse("get_reaction",None,["TestGame4","0","2a8a524a-7485-4c99-8672-99e05fb92c2d"]))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class LoadGamesTestCase(APITestCase):

    def test(self):
        response = self.client.get(reverse("get_games",None))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class PostPerceiveTestCase(APITestCase):

    def setUp(self):
        #self.view= perceive
        self.url=reverse("post_perceive",None,["game1","0"])

    # def test_post(self):
    #     response = self.client.get(self.url)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_creation(self):


        sample_data = {
  "perceived_info": [
    {
      "persona": "고영이",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "고영이",
            None,
            None,
            None
          ]
        },
        {
          "dist": 1.60030615,
          "event": [
            "이화령",
        None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "김태리",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "김태리",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "나주교",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 1.48961639,
          "event": [
            "오화가",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "변호인",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "변호인",
            None,
            None,
            None
          ]
        },
        {
          "dist": 2.60976577,
          "event": [
            "최문식",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "여이삭",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "여이삭",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "오서달",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "오서달",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "오화가",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 1.48961639,
          "event": [
            "나주교",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "유리코",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "유태호",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "유태호",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "이자식",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "이자식",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "유리코",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "이장남",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "이장남",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "이지양",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "이지양",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "이화령",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "이화령",
            None,
            None,
            None
          ]
        },
        {
          "dist": 1.60030615,
          "event": [
            "고영이",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "주아령",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "주아령",
            None,
            None,
            None
          ]
        }
      ]
    },
    {
      "persona": "최문식",
      "curr_address": "home:home:home:home",
      "perceived_tiles": [
        {
          "dist": 0.0,
          "event": [
            "최문식",
            None,
            None,
            None
          ]
        },
        {
          "dist": 2.60976577,
          "event": [
            "변호인",
            None,
            None,
            None
          ]
        }
      ]
    }
  ],
  "meta": {
    "curr_time": "2024-08-01T08:01:48"
  }
}


        #sample_data = {"title": "Sample title", "content": "Sample content"}
        #json.dump(sample_data)
        #JSONRenderer().render(sample_data)
        #print(sample_data)
        response = self.client.post(self.url, sample_data, format ='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        

# class PostGameStartTestCase(APITestCase):

#     def setUp(self):
#         #self.view= perceive
#         self.url=reverse("game_start",None)

#     # def test_post(self):
#     #     response = self.client.get(self.url)

#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_creation(self):


    #     sample_data = {	
    #         "sim_code" : "agenti", #base -> assembly_attendance 에러가 남(base scratch는 수정 안됐으니까.) agenti -> 나주교 에러가남.
	# 		"game_name": "gameTest01161" 
	# 	}

    #     sample_data["game_name"] = "gameTestRandom"+str(random.randint(1, 100))

    #     response = self.client.post(self.url, sample_data, format ='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
   
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *


class GameStageCreationTestCase(APITestCase):
    def setUp(self):
        # 테스트를 위한 사용자 생성
        self.user = MyUser.objects.create(username='testuser')
        self.url = reverse('create-game-stage')
    
    def test_create_game_stage_with_valid_data(self):
        """
        유효한 데이터로 GameStage 객체를 생성하는 경우를 테스트합니다.
        """
        data = {
            'user': self.user.uuid,
            'game_name': 'TestGame2',
            'sim_code': 'agenti',
            'is_completed': False #필수 필드 아님
        }
        response = self.client.post(self.url, data, format='json')
        
        # 성공적으로 객체가 생성되었는지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GameStage.objects.count(), 1)
        self.assertEqual(GameStage.objects.get().game_name, 'TestGame')

    def test_create_game_stage_with_invalid_data(self):
        """
        유효하지 않은 데이터(예: 필수 필드 누락)로 GameStage 객체를 생성하려는 경우를 테스트합니다.
        """
        data = {
            # 'user' 필드 누락
            'game_name': 'TestGame',
            'sim_code': 'agenti_15',
            'is_completed': False
        }
        response = self.client.post(self.url, data, format='json')
        
        # 데이터가 유효하지 않으므로 객체 생성이 실패했는지 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserCreationTestCase(APITestCase):
    def test_create_user_with_valid_username(self):
        """
        유효한 username으로 사용자를 생성하는 경우를 테스트합니다.
        """
        url = reverse('registration')
        data = {'username': 'testuser'}
        response = self.client.post(url, data, format='json')
        
        # 성공적으로 사용자가 생성되었는지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(MyUser.objects.get().username, 'testuser')

    def test_create_user_with_invalid_data(self):
        """
        유효하지 않은 데이터(예: username 누락)로 사용자를 생성하려는 경우를 테스트합니다.
        """
        url = reverse('registration')
        data = {}  # username 누락
        response = self.client.post(url, data, format='json')
        
        # 데이터가 유효하지 않으므로 사용자 생성이 실패했는지 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


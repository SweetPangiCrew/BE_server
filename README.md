
### 스윗팡이크루팀의 Agent.I 백엔드 장고 서버 레파지토리

## 1. 클라우드 API 서버 링크 

http://52.14.83.66:8000/swagger

## 2. 로컬 서버 Build 방법 

1) Github의 코드를 Clone한다.
2) 파이썬 설치 후 아래 라이브러리를 터미널에서 설치한다. 
   라이브러리 설치는 터미널에서 클론한 폴더 경로 아래에서 가능하다.
$ ~/BE_server> pip3 install Django
$ ~/BE_server> pip install -r requirements.txt


터미널에서 클론한 폴더 경로로 이동 후 my_settings.py를 생성한다. 

$ cd backend_server

my_settings.py 파일안에 아래 내용을 입력한다.
''' 
SECRET_KEY = "장고 SECRET KEY"
openai_key = "OPEN AI KEY 입력"
'''


# 정상 작동 테스트 방법 

npc/movemenet/{sim_code}/{step}/{user}를 클릭하고
아래 파라미터를 다음과 같이 채운다. 

sim_code : 1
step : 1 
user : d49a4101-0d8b-430e-894a-10f8ed2d65d0

채운 후 Execute를 누르면 결과 값을 받아올 수 있다.


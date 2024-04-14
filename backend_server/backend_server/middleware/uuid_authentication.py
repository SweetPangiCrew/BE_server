from django.http import JsonResponse
from users.models import MyUser

class UUIDAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 요청 헤더에서 UUID를 추출
        user_uuid = request.headers.get('X-User-UUID')

        if user_uuid:
            try:
                # UUID로 사용자 인증
                user = MyUser.objects.get(uuid=user_uuid)
                request.user = user
            except MyUser.DoesNotExist:
                # UUID가 유효하지 않은 경우
                return JsonResponse({'error': 'Invalid UUID'}, status=401)

        response = self.get_response(request)
        return response


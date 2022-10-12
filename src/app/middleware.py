import jwt
from .models import Client
from django.utils.deprecation import MiddlewareMixin

JWT_SECRET = "TOP SECRET"


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def __int__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            authorization_token = request.headers.get("authorization")
            payload = jwt.decode(authorization_token, JWT_SECRET, algorithms=["HS256"])
            client = Client.objects.get(login=payload["login"])
            request.client = client
        except:
            request.client = None

        response = self.get_response(request)
        return response

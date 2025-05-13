from django.http import HttpRequest
from accounts.models import Token, User


class PasswordlessAuthenticationBackend:
    def authenticate(self, request: HttpRequest, uid: str) -> (User | None):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)

        except User.DoesNotExist:
            return User.objects.create(email=token.email)

        except Token.DoesNotExist:
            return None


    def get_user(self, email: str) -> (User | None):
        try:
            return User.objects.get(email=email)
        
        except User.DoesNotExist:
            return None

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand, CommandParser
from typing import Any


User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("email")

    
    def handle(self, *args: Any, **options: Any) -> None:
        session_key = create_pre_authenticated_session(options["email"])
        self.stdout.write(session_key)


def create_pre_authenticated_session(email: str) -> str:
    user, _ = User.objects.get_or_create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key

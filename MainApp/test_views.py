import pytest
from django.contrib.auth.models import User, AnonymousUser

from .views import add_snippet_page

from django.test import Client, RequestFactory
from django.urls import reverse
from .models import Snippet

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware


def add_messages_and_session_to_request(request):
    # Attach session for messages to work correctly
    middleware = SessionMiddleware(lambda r: None)  # Mock the get_response callable
    middleware.process_request(request)
    request.session.save()  # Ensure a session key is generated

    # Attach message storage
    setattr(request, '_messages', FallbackStorage(request))


class TestIndexPage:
    def test_index_page(self):
        client = Client()
        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert 'Добро пожаловать' in response.content.decode()
        assert response.context.get('pagename') == 'PythonBin'


@pytest.mark.django_db
class TestAddSnippetPage:
    def setup_method(self, method):
        self.factory = RequestFactory()

    def test_anonymous_user(self):
        request = self.factory.get(reverse('snippet-add'))
        request.user = AnonymousUser()
        response = add_snippet_page(request)

        assert response.status_code == 302

    def test_authenticated_user(self):
        request = self.factory.get(reverse('snippet-add'))
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass12345",
        )
        request.user = user
        response = add_snippet_page(request)

        assert response.status_code == 200
        # assert 'Добро пожаловать' in response.content.decode()
        # assert response.context.get('pagename') == 'PythonBin'

    def test_post_form_data(self):
        form_data = {
            "name": "Test form snippet",
            "lang": "python",
            "code": "print('Hello, world!')",
            "public": True,
        }
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass12345",
        )

        request = self.factory.post(reverse('snippet-add'), form_data)
        request.user = user
        add_messages_and_session_to_request(request)
        response = add_snippet_page(request)

        snippet = Snippet.objects.get(id=1)

        assert response.status_code == 302
        assert snippet.name == form_data['name']
        assert snippet.lang == form_data['lang']
        assert snippet.code == form_data['code']
        assert snippet.public == form_data['public']

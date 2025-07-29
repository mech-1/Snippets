import pytest
from .models import Snippet
from django.contrib.auth.models import User

@pytest.mark.django_db
class TestSnippetModel:
    def test_snippet_creation(self):
        Snippet.objects.create(
            name="Test Snippet",
            lang="python",
            code="print('Hello World!')",
            public=True,
        )

        snippet = Snippet.objects.get(id=1)

        assert snippet.name == "Test Snippet"
        assert snippet.lang == "python"
        assert snippet.code == "print('Hello World!')"
        assert snippet.public is True
        assert snippet.views_count == 0

    def test_user_snippet_creation(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass12345",
        )

        snippet = Snippet.objects.create(
            name="User Snippet",
            lang="javascript",
            code="console.log('Hello World!')",
            user=user,
            public=False,
        )

        assert snippet.name == "User Snippet"
        assert snippet.lang == "javascript"
        assert snippet.code == "console.log('Hello World!')"
        assert snippet.user.username == "testuser"
        assert not snippet.public
        assert snippet.views_count == 0

import pytest
from django.contrib.auth.models import User, AnonymousUser
from MainApp.factories import UserFactory, SnippetFactory, CommentFactory, TagFactory

from MainApp.models import Snippet, Tag, Comment


# Factory Users
@pytest.fixture
def user_factory():
    def _create_user(username) -> User:
        return UserFactory(username=username)

    return _create_user


# использование фабрики в тесте
@pytest.mark.django_db
def test_create_user2(user_factory):
    user = user_factory("Ivan")
    assert user.username == "Ivan"


# Factory Snippets
@pytest.fixture
def user():
    """Фикстура для создания пользователя"""
    return UserFactory()


@pytest.fixture
def snippets_factory():
    def _create_snippets(n=5, user=None):
        return SnippetFactory.create_batch(n, user=user)

    return _create_snippets


@pytest.mark.django_db
def test_create_snippets(snippets_factory):
    snippets_factory()
    snippets = Snippet.objects.all()
    assert snippets.count() == 5
    for snippet in snippets:
        assert snippet.user is None


@pytest.mark.django_db
def test_create_snippets_with_user(snippets_factory, user):
    snippets_factory(n=4, user=user)
    snippets = Snippet.objects.all()
    assert snippets.count() == 4
    for snippet in snippets:
        assert snippet.user == user


# Tags Factory
@pytest.fixture
def tags_factory():
    def _create_tags(names: list):
        tags = []
        for name in names:
            tags.append(TagFactory.create(name=name))
        return tags

    return _create_tags


@pytest.mark.django_db
def test_create_tags(tags_factory):
    # # Создаст три тега, с указанными именами
    tags = tags_factory(names=["js", "basic", "oop"])
    assert Tag.objects.count() == 3
    assert len(tags) == 3


@pytest.fixture
def snippet():
    return SnippetFactory()

@pytest.fixture
def comments_factory():
    def _create_comments_to_snippet(snippet, n: int):
        return CommentFactory.create_batch(n, snippet=snippet)

    return _create_comments_to_snippet

@pytest.mark.django_db
def test_create_comments_to_snippet(comments_factory, snippet):
    comments = comments_factory(snippet=snippet, n=6)
    assert len(comments) == 6
    assert Comment.objects.count() == 6
    for comment in Comment.objects.all():
        assert comment.snippet == snippet
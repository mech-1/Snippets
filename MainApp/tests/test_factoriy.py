import pytest
from MainApp.factories import *
from MainApp.models import User

@pytest.mark.django_db
def test_task1():
    UserFactory(username="Alice")
    user = User.objects.get(username="Alice")
    assert user.username == "Alice"

# def test_task2():
#     TagFactory().
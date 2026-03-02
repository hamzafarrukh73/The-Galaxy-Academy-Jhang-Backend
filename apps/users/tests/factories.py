import factory
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory

from ..models import User


class UserFactory(DjangoModelFactory["User"]):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.django.Password("password123")  # type: ignore

    is_active = True
    is_staff = False
    is_superuser = False


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class GroupFactory(DjangoModelFactory["Group"]):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"group{n}")

import uuid
from enum import Enum
from typing import Optional, Set

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import Model


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self, username: str, password: str, roles: Set[str], **extra_fields
    ):
        if not username:
            raise ValueError("The given username must be set")
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        for role in roles:
            r, _ = Role.objects.get_or_create(name=role)
            user.roles.add(r)

        return user

    def create_user(
            self,
            username: str,
            password=None,
            roles: Optional[Set[str]] = None,
            **extra_fields
    ):
        roles = roles or set()
        user = self._create_user(username, password, roles, **extra_fields)
        return user

    def create_superuser(self, username: str, password: str, **extra_fields):
        user = self.create_user(username, password, {"admin"}, **extra_fields)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
    )
    first_name = models.CharField(max_length=30, blank=True)
    second_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField("Role", related_name="users")

    objects = UserManager()

    USERNAME_FIELD = "username"

    def _contains_role(self, role: "RolesEnum") -> bool:
        try:
            self.roles.get(name=role.value[0])
        except Role.DoesNotExist:
            return False
        else:
            return True

    @property
    def is_uploader(self) -> bool:
        return self._contains_role(RolesEnum.uploader)

    @property
    def is_admin(self) -> bool:
        return self._contains_role(RolesEnum.admin)


class Uploader(Model):
    id = models.OneToOneField(
        User, primary_key=True, related_name="uploader", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.id.username


class Admin(Model):
    id = models.OneToOneField(
        User, primary_key=True, related_name="admin", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.id.username


class RolesEnum(Enum):
    uploader = ("uploader", Uploader)
    admin = ("admin", Admin)


class Role(Model):
    name = models.CharField(
        primary_key=True,
        max_length=16,
        choices=[(role.value[0], role.value[0]) for role in RolesEnum],
    )

    def __str__(self):
        return self.name

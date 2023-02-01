from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from toDoMateProject.storage_backends import PublicMediaStorage
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=50, default='사용자', blank=False)
    detail = models.CharField(max_length=200, blank=True)
    # private과 public 중 어떤 것을 할지 몰라 일단 public으로 설정했습니다.
    image = models.ImageField(storage=PublicMediaStorage())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Code(models.Model):
    code = models.IntegerField()
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)

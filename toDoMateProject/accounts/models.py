from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from toDoMateProject.storeage_backends import PublicMediaStorage
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=50, blank=True)
    detail = models.CharField(max_length=200, blank=True)
    # private과 public 중 어떤 것을 할지 몰라 일단 public으로 설정했습니다.
    if settings.USE_S3:
        image = models.ImageField(storage=PublicMediaStorage())
    else:
        image = models.ImageField(default='default.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


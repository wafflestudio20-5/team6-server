from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=50, blank=True)
    detail = models.CharField(max_length=200, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Task(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50, blank=False, null=False)
    complete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

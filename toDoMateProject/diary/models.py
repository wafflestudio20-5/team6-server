from django.db import models

from accounts.models import User


# Create your models here.
class Diary(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=50, blank=False, null=False)
    context = models.CharField(max_length=500, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)


class Comment(models.Model):
    context = models.CharField(max_length=500, blank=False, null=False)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    nickname = models.CharField(max_length=50, blank=True)
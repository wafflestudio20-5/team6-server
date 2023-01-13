from django.db import models

from accounts.models import User


# Create your models here.
class Diary(models.Model):
    date = models.DateField(unique=True)
    context = models.CharField(max_length=500, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
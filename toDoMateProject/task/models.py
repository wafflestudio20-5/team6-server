from django.db import models

from accounts.models import User


# Create your models here.
class Task(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50, blank=False, null=False)
    complete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    #repeated = models.IntegerField(default=0)
from django.db import models
from accounts.models import User


# Create your models here.
#read_by: 0(Owner Only), 1(Followers) // 2(All Users)
class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    #read_by = models.IntegerField(default=0)


class Task(models.Model):
    date = models.DateField()
    # start_date = models.DateField()
    # end_date = models.DateField()
    # delta_time = models.DateTimeField()
    name = models.CharField(max_length=50, blank=False, null=False)
    complete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)


# class Repeat(models.Model):
#     name = models.CharField(max_length=50, blank=False, null=False)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)

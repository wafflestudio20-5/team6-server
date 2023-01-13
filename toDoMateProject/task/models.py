from django.db import models
from accounts.models import User


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # @classmethod
    # def get_default_pk(cls):
    #     exam, created = cls.objects.get_or_create(
    #         name='common',
    #         defaults=dict(description='this is not an exam'),
    #     )
    #     return exam.pk


class Task(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50, blank=False, null=False)
    complete = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)


# class Repeat(models.Model):
#     name = models.CharField(max_length=50, blank=False, null=False)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)

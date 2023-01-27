from django.db import models


from accounts.models import User
# Create your models here.

class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    
    class Meta:
        db_table = 'follow'


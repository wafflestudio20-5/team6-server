from django.db import models


from accounts.models import User
# Create your models here.

class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    
    class Meta:
        db_table = 'follow'

class Block(models.Model):
    block_from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block_from_user')
    block_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block_to_user')
    
    class Meta:
        db_table = 'block'
        
from rest_framework import serializers

from follow.models import Follow
from accounts.models import User

class FolloweeSerializer(serializers.ModelSerializer):
    to_user_email = serializers.EmailField()
    to_user_id = serializers.IntegerField()
    
    def to_representation(self, data):
        response = {'to_user_email' : data.to_user.email,
                    'to_user_id' : data.to_user.id}
        return response

    class Meta:
        model = Follow
        fields = ['from_user_email', 'to_user_email', 'from_user_id', 'to_user_id']
        
class FollowerSerializer(serializers.ModelSerializer):
    from_user_email = serializers.EmailField()
    from_user_id = serializers.IntegerField()
    
    def to_representation(self, data):
        response = {'from_user_email' : data.from_user.email,
                    'from_user_id' : data.from_user.id}
        return response

    class Meta:
        model = Follow
        fields = ['from_user_email', 'to_user_email', 'from_user_id', 'to_user_id']
        

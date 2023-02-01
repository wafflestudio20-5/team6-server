from rest_framework import serializers

from follow.models import Follow
from accounts.models import User

class FolloweeSerializer(serializers.ModelSerializer):
    to_user_email = serializers.EmailField()
    to_user_id = serializers.IntegerField()
    to_user_nickname = serializers.CharField()

    def to_representation(self, data):
        response = {'to_user_email' : data.to_user.email,
                    'to_user_id' : data.to_user.id,
                    'to_user_nickname' : data.to_user.nickname}
        return response

    class Meta:
        model = Follow
        fields = ['from_user_email', 'to_user_email', 'from_user_id', 'to_user_id', 'from_user_nickname', 'to_user_nickname']

        
class FollowerSerializer(serializers.ModelSerializer):
    from_user_email = serializers.EmailField()
    from_user_id = serializers.IntegerField()
    from_user_nickname = serializers.CharField()
    
    def to_representation(self, data):
        response = {'from_user_email' : data.from_user.email,
                    'from_user_id' : data.from_user.id,
                    'from_user_nickname' : data.from_user.nickname}
        return response

    class Meta:
        model = Follow
        fields = ['from_user_email', 'to_user_email', 'from_user_id', 'to_user_id', 'from_user_nickname', 'to_user_nickname']
        

class BlockUserSerializer(serializers.ModelSerializer):
    to_user_email = serializers.EmailField()
    to_user_id = serializers.IntegerField()
    to_user_nickname = serializers.CharField()
    
    def to_representation(self, data):
        response = {'to_user_email' : data.block_to_user.email,
                    'to_user_id' : data.block_to_user.id,
                    'to_user_nickname' : data.block_to_user.nickname}
        return response

    class Meta:
        model = Follow
        fields = ['from_user_email', 'to_user_email', 'from_user_id', 'to_user_id', 'from_user_nickname', 'to_user_nickname']
        
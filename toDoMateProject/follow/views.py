import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status



from accounts.models import User
from accounts.serializers import UserDetailSerializer
from follow.models import Follow
from follow.serializers import FollowerSerializer, FolloweeSerializer
from django.shortcuts import redirect, get_object_or_404

# BASE_URL = "http://ec2-3-38-100-94.ap-northeast-2.compute.amazonaws.com:8000"
BASE_URL = "http://3.38.100.94"


class FollowerListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(User, id=uid)
        followers = Follow.objects.filter(to_user=user)
        return followers

    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    

class FolloweeListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(User, id=uid)
        followers = Follow.objects.filter(from_user=user)
        return followers

    permission_classes = [IsAuthenticated]
    serializer_class = FolloweeSerializer
    

@api_view(['POST'])
def follow_user(request, *args, **kwargs):
    uid = request.user.id
    fid = request.data['followee']
    follower = get_object_or_404(User, id=uid)
    followee = get_object_or_404(User, id=fid)
    try:
        relation = Follow.objects.get(from_user=follower, to_user=followee)
        return Response(data='', status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        relation = Follow.objects.create(from_user=follower, to_user=followee)
        content = {"detail" : f"user {uid} follows user {fid}"}
        return Response(data=content, status=status.HTTP_201_CREATED)


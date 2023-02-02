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
from follow.models import Follow, Block
from follow.serializers import FollowerSerializer, FolloweeSerializer, BlockUserSerializer, BlockedUserSerializer
from django.shortcuts import redirect, get_object_or_404


class FollowerListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(User, id=uid)
        followers = Follow.objects.filter(to_user=user)[::-1]
        return followers

    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer
    

class FolloweeListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(User, id=uid)
        followers = Follow.objects.filter(from_user=user)[::-1]
        return followers

    permission_classes = [IsAuthenticated]
    serializer_class = FolloweeSerializer


class FollowerDetailView(generics.RetrieveDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        f_user = get_object_or_404(User, id=self.kwargs['fid'])
        try:
            followers = Follow.objects.get(from_user=f_user, to_user=self.request.user)
            return followers
        except Follow.DoesNotExist:
            return None
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'detail' : f"{self.kwargs['fid']} is not following {self.request.user.id}."}, status=status.HTTP_200_OK)
        self.perform_destroy(instance)
        content = {'detail' : None}
        return Response(data=content, status=status.HTTP_200_OK)
                
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'is_following' : False}, status=status.HTTP_200_OK)
        return Response(data={'is_following' : True}, status=status.HTTP_200_OK)
    
    permission_classes = [IsAuthenticated]
    serializer_class = FollowerSerializer    


class FolloweeDetailView(generics.RetrieveDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        f_user = get_object_or_404(User, id=self.kwargs['fid'])
        try:
            followers = Follow.objects.get(from_user=self.request.user, to_user=f_user)
            return followers
        except Follow.DoesNotExist:
            return None
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'detail' : f"{self.request.user.id} is not following {self.kwargs['fid']}."}, status=status.HTTP_200_OK)
        self.perform_destroy(instance)
        content = {'detail' : None}
        return Response(data=content, status=status.HTTP_200_OK)
                
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'is_following' : False}, status=status.HTTP_200_OK)
        return Response(data={'is_following' : True}, status=status.HTTP_200_OK)
    
    permission_classes = [IsAuthenticated]
    serializer_class = FolloweeSerializer


class BlockUserListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(User, id=uid)
        blocks = Block.objects.filter(block_from_user=user)[::-1]
        return blocks

    permission_classes = [IsAuthenticated]
    serializer_class = BlockUserSerializer


class BlockDetailView(generics.RetrieveDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        b_user = get_object_or_404(User, id=self.kwargs['fid'])
        try:
            blocks = Block.objects.get(block_from_user=self.request.user, block_to_user=b_user)
            return blocks
        except Block.DoesNotExist:
            return None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'detail' : f"{self.request.user.id} is not blocking {self.kwargs['fid']}."}, status=status.HTTP_200_OK)
        self.perform_destroy(instance)
        content = {'detail' : None}
        return Response(data=content, status=status.HTTP_200_OK)
            
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'is_blocking' : False}, status=status.HTTP_200_OK)
        return Response(data={'is_blocking' : True}, status=status.HTTP_200_OK)
    
    permission_classes = [IsAuthenticated]
    serializer_class = BlockUserSerializer
        

class BlockedUserListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        user = get_object_or_404(User, id=uid)
        blocks = Block.objects.filter(block_to_user=user)[::-1]
        return blocks

    permission_classes = [IsAuthenticated]
    serializer_class = BlockedUserSerializer


class BlockedDetailView(generics.RetrieveAPIView):
    def get_object(self):
        uid = self.request.user.id
        b_user = get_object_or_404(User, id=self.kwargs['fid'])
        try:
            blocks = Block.objects.get(block_from_user=b_user, block_to_user=self.request.user)
            return blocks
        except Block.DoesNotExist:
            return None
            
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == None:
            return Response(data={'is_blocking' : False}, status=status.HTTP_200_OK)
        return Response(data={'is_blocking' : True}, status=status.HTTP_200_OK)
    
    permission_classes = [IsAuthenticated]
    serializer_class = BlockedUserSerializer


@api_view(['POST'])
def follow_user(request, *args, **kwargs):
    uid = request.user.id
    fid = request.data['followee']
    if uid == fid:
        return Response(data={"detail" : "You can't follow your self."}, status=status.HTTP_400_BAD_REQUEST)
    
    follower = get_object_or_404(User, id=uid)
    followee = get_object_or_404(User, id=fid)
    
    try:
        block = Block.objects.get(block_from_user=followee, block_to_user=follower)
        return Response(data={'detail' : f"{uid} blocked {fid}."}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:    
        try:
            relation = Follow.objects.get(from_user=follower, to_user=followee)
            return Response(data={'detail' : f"{uid} already follows {fid}."}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            relation = Follow.objects.create(from_user=follower, to_user=followee)
            content = {"detail" : f"user {uid} follows user {fid}"}
            return Response(data=content, status=status.HTTP_201_CREATED)

    
@api_view(['POST'])
def block_user(request, *args, **kwargs):
    uid = request.user.id
    fid = request.data['follower']
    followee = get_object_or_404(User, id=uid)
    follower = get_object_or_404(User, id=fid)
    try:
        block = Block.objects.get(block_from_user=followee, block_to_user=follower)
        content = {"detail" : f"user {uid} already blocked user {fid}"}
        return Response(data=content, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        block = Block.objects.create(block_from_user=followee, block_to_user=follower)
    
    try:
        relation = Follow.objects.get(from_user=follower, to_user=followee)
        relation.delete()
    except ObjectDoesNotExist:
        pass
    
    try:
        relation = Follow.objects.get(from_user=followee, to_user=follower)
        relation.delete()
    except ObjectDoesNotExist:
        pass
    
    content = {"detail" : f"user {uid} blocked user {fid}"}
    return Response(data=content, status=status.HTTP_200_OK)

    
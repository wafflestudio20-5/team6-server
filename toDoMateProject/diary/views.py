from django.db.models import TextField
from django.db.models.functions import Cast
from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.models import User
from follow.models import Block
from diary.models import Diary, Comment
from diary.permissions import IsOwnerOrReadOnly, is_following
from diary.serializers import DiaryListSerializer, DiaryListCreateSerializer, DiaryRetrieveUpdateDeleteSerializer, \
    CommentListCreateSerializer, CommentRetrieveUpdateDestroySerializer

from accounts.models import User
from accounts.serializers import UserDetailSerializer
from rest_framework.response import Response
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotFound
import json

# BASE_URL = "http://ec2-3-38-100-94.ap-northeast-2.compute.amazonaws.com:8000"
BASE_URL = "http://3.38.100.94"

# Create your views here.
class DiaryListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        return Diary.objects.filter(created_by_id=uid).annotate(str_date=Cast('date', TextField()))

    serializer_class = DiaryListSerializer
    permission_classes = [IsAuthenticated]


class DiaryListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        date = self.kwargs['date']
        return Diary.objects.filter(created_by_id=uid, date=date).annotate(str_date=Cast('date', TextField()))

    serializer_class = DiaryListCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        uid = self.request.user.id
        date = self.kwargs['date']
        nickname = User.objects.get(id=uid).nickname
        serializer.save(created_by_id=uid, date=date, nickname=nickname)


class DiaryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        date = self.kwargs['date']
        return Diary.objects.filter(created_by_id=uid, date=date).annotate(str_date=Cast('date', TextField())).first()

    serializer_class = DiaryRetrieveUpdateDeleteSerializer
    lookup_field = 'date'
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def diary_redirect(request, *args, **kwargs):
    uid = request.user.id
    date = kwargs.get('date')
    diary = Diary.objects.filter(created_by_id=uid, date=date).first()

    if diary:
        return redirect(BASE_URL + f"/diary/mydiary/{date}/update")
    else:
        return redirect(BASE_URL + f"/diary/mydiary/{date}/create")


class DiaryWatchView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        did = self.kwargs['did']
        diary = Diary.objects.filter(id=did).annotate(str_date=Cast('date', TextField())).first()
        self.check_object_permissions(self.request, diary)
        return diary

    serializer_class = DiaryRetrieveUpdateDeleteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticated]
    lookup_field = 'did'


class CommentListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        did = self.kwargs['did']
        diary = Diary.objects.get(id=did)
        self.check_object_permissions(self.request, diary)
        comment = Comment.objects.filter(diary_id=did).annotate(str_created_at=Cast('created_at', TextField()), str_updated_at=Cast('updated_at', TextField())).order_by('created_at')
        return comment

    serializer_class = CommentListCreateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        uid = self.request.user.id
        did = self.kwargs['did']
        nickname = User.objects.get(id=uid).nickname
        serializer.save(diary_id=did, created_by_id=uid, nickname=nickname)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        cid = self.kwargs['cid']
        comment = Comment.objects.filter(id=cid).annotate(str_created_at=Cast('created_at', TextField()), str_updated_at=Cast('updated_at', TextField())).first()
        self.check_object_permissions(self.request, comment.diary)
        return comment

    serializer_class = CommentRetrieveUpdateDestroySerializer
    permission_classes = [IsOwnerOrReadOnly]
    

def get_user_by_email(email):
    selected_user = get_object_or_404(User, email=email)
    return selected_user


class DiarySearchListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.kwargs['uid']
        if is_following(self.request, uid):
            return Diary.objects.filter(created_by_id=uid).annotate(str_date=Cast('date', TextField()))
        else:
            return ['No permission']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset == ['No permission']:
            return Response({"detail" : "No permission(folllow)."}, status=status.HTTP_401_UNAUTHORIZED)
                
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    serializer_class = DiaryListSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    
class DiarySearchDateListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.kwargs['uid']
        date = self.kwargs['date']
        if is_following(self.request, uid):
            queryset = Diary.objects.filter(created_by_id=uid, date=date).annotate(str_date=Cast('date', TextField()))
            return queryset
        else:
            return ['No permission']
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset == ['No permission']:
            return Response({"detail" : "No permission(folllow)."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # if queryset == ['Empty queryset']:
        #     date = self.kwargs['date']
        #     content = {"detail" : f"No task found({date})."}
        #     return HttpResponseBadRequest(json.dumps(content), content_type='application/json')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    serializer_class = DiaryListSerializer
    permission_classes = [IsAuthenticated]
  
  
class SearchUserDetailView(generics.RetrieveAPIView):
    def get_object(self):
        email = self.kwargs['email']
        if not email:
            return "Email Not Found"
        
        try:
            user = User.objects.get(email=email)
            if user.id == self.request.user.id:
                return "It's me"
            ret = user
        except User.DoesNotExist:
            return "User Not Found"

        try:
            block = Block.objects.get(block_from_user=user, block_to_user=self.request.user)
            return "Blocked"
        except Block.DoesNotExist:
            # return ret
            try:
                block = Block.objects.get(block_from_user=self.request.user, block_to_user=user)
                return "Blocked"
            except Block.DoesNotExist:
                return ret

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == "Email Not Found":
            content = {"detail" : "There's no email data."}
            return Response(data=content, status=status.HTTP_404_NO_CONTENT)
        if instance == "User Not Found":
            content = {'detail' : f'User({self.kwargs["email"]}) not found'}
            return Response(data=content, status=status.HTTP_200_OK)
        if instance == "It's me":
            content = {'detail' : None}
            return Response(data=content, status=status.HTTP_200_OK)
        if instance == 'Blocked':
            content = {'detail' : 'blocked'}
            return Response(data=content, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

from django.db.models import TextField
from django.db.models.functions import Cast
from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from diary.models import Diary, Comment
from diary.permissions import IsOwnerOrReadOnly
from diary.serializers import DiaryListSerializer, DiaryListCreateSerializer, DiaryRetrieveUpdateDeleteSerializer, \
    CommentListCreateSerializer, CommentRetrieveUpdateDestroySerializer


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


def diary_redirect(request, *args, **kwargs):
    uid = request.user.id
    date = kwargs.get('date')
    diary = Diary.objects.filter(created_by_id=uid, date=date).first()

    if diary:
        return redirect(f"http://3.38.100.94/diary/mydiary/{date}/update")
    else:
        return redirect(f"http://3.38.100.94/diary/mydiary/{date}/create")


class DiaryWatchView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        did = self.kwargs['did']
        diary = Diary.objects.filter(id=did).annotate(str_date=Cast('date', TextField())).first()
        self.check_object_permissions(self.request, diary)
        return diary

    serializer_class = DiaryRetrieveUpdateDeleteSerializer
    permission_classes = [IsOwnerOrReadOnly]
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
        serializer.save(diary_id=did, created_by_id=uid)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        cid = self.kwargs['cid']
        comment = Comment.objects.filter(id=cid).annotate(str_created_at=Cast('created_at', TextField()), str_updated_at=Cast('updated_at', TextField())).first()
        self.check_object_permissions(self.request, comment.diary)
        return comment

    serializer_class = CommentRetrieveUpdateDestroySerializer
    permission_classes = [IsOwnerOrReadOnly]
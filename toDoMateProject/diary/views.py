from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics

from diary.models import Diary, Comment
#from diary.permissions import IsOwnerOrReadOnly
from diary.serializers import DiaryListSerializer, DiaryCreateSerializer, DiaryRetrieveUpdateDeleteSerializer, \
    CommentListCreateSerializer, CommentRetrieveUpdateDestroySerializer


# Create your views here.
class DiaryListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        return Diary.objects.filter(created_by_id=uid)

    serializer_class = DiaryListSerializer
    #permission_classes = [IsOwnerOrReadOnly]


class DiaryCreateView(generics.CreateAPIView):
    serializer_class = DiaryCreateSerializer
    #permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        uid = self.request.user.id
        date = self.kwargs['date']
        serializer.save(created_by_id=uid, date=date)


class DiaryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        date = self.kwargs['date']
        return Diary.objects.get(created_by_id=uid, date=date)

    serializer_class = DiaryRetrieveUpdateDeleteSerializer
    lookup_field = 'date'
    #permission_classes = [IsOwnerOrReadOnly]


def diary_redirect(request, *args, **kwargs):
    date = kwargs.get('date')
    diary = Diary.objects.filter(date=date).first()

    if diary:
        return redirect(f"http://127.0.0.1:8000/diary/mydiary/{date}/update")
    else:
        return redirect(f"http://127.0.0.1:8000/diary/mydiary/{date}/create")


class DiaryWatchView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        did = self.kwargs['did']
        return Diary.objects.get(id=did)

    serializer_class = DiaryRetrieveUpdateDeleteSerializer
    lookup_field = 'did'


class CommentListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        did = self.kwargs['did']
        return Comment.objects.filter(diary_id=did).order_by('created_at')

    serializer_class = CommentListCreateSerializer

    def perform_create(self, serializer):
        uid = self.request.user.id
        did = self.kwargs['did']
        serializer.save(diary_id=did, created_by_id=uid)

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        cid = self.kwargs['cid']
        return Comment.objects.get(id=cid)

    serializer_class = CommentRetrieveUpdateDestroySerializer
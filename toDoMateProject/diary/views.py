from django.shortcuts import redirect
from rest_framework import generics

from diary.models import Diary
from diary.serializers import DiaryListSerializer, DiaryCreateSerializer, DiaryRetrieveUpdateDeleteSerializer


# Create your views here.
class DiaryListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        return Diary.objects.filter(created_by_id=uid)

    serializer_class = DiaryListSerializer
    #permission_classes = [IsAuthenticated]


class DiaryCreateView(generics.CreateAPIView):
    serializer_class = DiaryCreateSerializer
    #permission_classes = [IsAuthenticated]

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
    #permission_classes = [IsAuthenticated]


def diary_redirect(request, *args, **kwargs):
    date = kwargs.get('date')
    diary = Diary.objects.filter(date=date).first()

    if diary:
        return redirect(f"http://127.0.0.1:8000/diary/{date}/update")
    else:
        return redirect(f"http://127.0.0.1:8000/diary/{date}/create")
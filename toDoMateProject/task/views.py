import datetime

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics

from task.models import Task, Tag
from task.serializers import TaskUpdateNameSerializer, TaskUpdateDateSerializer, \
    TagListCreateSerializer, TaskDetailDestroySerializer, TaskListCreateSerializer, TaskListSerializer


# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        date = self.kwargs['date']
        return Task.objects.filter(created_by_id=uid, date=date).order_by('tag')
        #return Task.objects.filter(created_by_id=uid, repeated=0) | Task.objects.filter(created_by_id=uid, repeated=1)

    serializer_class = TaskListCreateSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        uid = self.request.user.id
        date = self.kwargs['date']
        serializer.save(created_by_id=uid, date=date)
        #serializer.save(created_by_id=uid, repeated=0)


class TaskListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        return Task.objects.filter(created_by_id=uid).order_by('date', 'tag')
        #return Task.objects.filter(created_by_id=uid, date=date, repeated=0) | Task.objects.filter(created_by_id=uid, date=date, repeated=1)

    serializer_class = TaskListSerializer
    #permission_classes = [IsAuthenticated]


class TaskDetailDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return get_object_or_404(Task, created_by_id=uid, id=tid)
        #return get_object_or_404(Task, created_by_id=uid, id=tid, repeated=0)

    serializer_class = TaskDetailDestroySerializer
    #permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']


class TaskUpdateNameView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return get_object_or_404(Task, created_by_id=uid, id=tid)

    serializer_class = TaskUpdateNameSerializer
    http_method_names = ['get', 'put']


class TaskUpdateDateView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return get_object_or_404(Task, created_by_id=uid, id=tid)

    serializer_class = TaskUpdateDateSerializer
    http_method_names = ['get', 'put']


def switch_complete(request, *args, **kwargs):
    uid = request.user.id
    tid = kwargs.get('tid')
    task = get_object_or_404(Task, created_by_id=uid, id=tid)
    task.complete = not task.complete
    task.save()
    return redirect(f"http://127.0.0.1:8000/task/detail/{tid}") #실제 url


def switch_tomorrow(request, *args, **kwargs):
    uid = request.user.id
    tid = kwargs.get('tid')
    task = get_object_or_404(Task, created_by_id=uid, id=tid)
    task.date = task.date + datetime.timedelta(days=1)
    task.save()
    return redirect(f"http://127.0.0.1:8000/task/detail/{tid}")  # 실제 url


class TagListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        return Tag.objects.filter(created_by_id=uid)

    serializer_class = TagListCreateSerializer

    def perform_create(self, serializer):
        uid = self.request.user.id
        serializer.save(created_by_id=uid)

# class RepeatListCreateView(generics.ListCreateAPIView):
#     def get_queryset(self):
#         uid = self.request.user.id
#         return Repeat.objects.filter(created_by_id=uid)
#
#     serializer_class = RepeatListCreateSerializer
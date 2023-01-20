import datetime

from django.db.models import TextField
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Cast

from task.models import Task#, Tag
from task.serializers import TaskUpdateNameSerializer, TaskUpdateDateSerializer, \
    TaskDetailDestroySerializer, TaskListCreateSerializer, TaskListSerializer


# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        # return Task.objects.filter(date=date).order_by('tag')
        uid = self.request.user.id
        date = self.kwargs['date']
        task = Task.objects.filter(created_by_id=uid, date=date).annotate(
            str_date=Cast('date', TextField())
        )
        return task
        #return Task.objects.filter(created_by_id=uid, repeated=0) | Task.objects.filter(created_by_id=uid, repeated=1)

    serializer_class = TaskListCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # date = self.kwargs['date']
        # serializer.save(date=date)
        uid = self.request.user.id
        date = self.kwargs['date']
        serializer.save(created_by_id=uid, date=date)
        #print('function called')
        #serializer.save(created_by_id=uid, repeated=0)


class TaskListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.request.user.id
        queryset = Task.objects.filter(created_by_id=uid).annotate(str_date=Cast('date', TextField())).order_by('date')
        return queryset

        #return Task.objects.filter(created_by_id=uid, date=date, repeated=0) | Task.objects.filter(created_by_id=uid, date=date, repeated=1)

    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]


class TaskDetailDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return Task.objects.filter(created_by_id=uid, id=tid).annotate(str_date=Cast('date', TextField())).first()
        #return get_object_or_404(Task, created_by_id=uid, id=tid, repeated=0)

    serializer_class = TaskDetailDestroySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete']


class TaskUpdateNameView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return Task.objects.filter(created_by_id=uid, id=tid).annotate(str_date=Cast('date', TextField())).first()

    serializer_class = TaskUpdateNameSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']


class TaskUpdateDateView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return Task.objects.filter(created_by_id=uid, id=tid).annotate(str_date=Cast('date', TextField())).first()

    serializer_class = TaskUpdateDateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']


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


# class TaskViewListView(generics.ListAPIView):
#     def get_queryset(self):
#         uid = self.kwargs['uid']
#         date = self.kwargs['date']
#         task_all = Task.objects.filter(created_by_id=uid, date=date, read_by=2)
#         task_follow = Task.objects.filter(created_by_id=uid, date=date, read_by=1)
#         task_owner = Task.objects.filter(created_by_id=uid, date=date, read_by=0)
#
#         return task_all
#
#     serializer_class = TaskViewListSerializer


# class TagListCreateView(generics.ListCreateAPIView):
#     def get_queryset(self):
#         uid = self.request.user.id
#         return Tag.objects.filter(created_by_id=uid)
#
#     serializer_class = TagListCreateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         uid = self.request.user.id
#         serializer.save(created_by_id=uid)
#
#
# class TagDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     def get_object(self):
#         uid = self.request.user.id
#         tid = self.kwargs['tid']
#         return get_object_or_404(Tag, created_by_id=uid, id=tid)
#
#     serializer_class = TagDetailUpdateDestroySerializer
#     permission_classes = [IsAuthenticated]


# class RepeatListCreateView(generics.ListCreateAPIView):
#     def get_queryset(self):
#         uid = self.request.user.id
#         return Repeat.objects.filter(created_by_id=uid)
#
#     serializer_class = RepeatListCreateSerializer
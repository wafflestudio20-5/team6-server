import datetime
import json

from django.db.models import TextField
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models.functions import Cast
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from task.permissions import IsOwnerOrReadOnly, is_following
from task.models import Task#, Tag
from task.serializers import TaskUpdateSerializer, \
    TaskDetailDestroySerializer, TaskListCreateSerializer, TaskListSerializer

# BASE_URL = "http://ec2-3-38-100-94.ap-northeast-2.compute.amazonaws.com:8000"
BASE_URL = "http://3.38.100.94"

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
        queryset = Task.objects.filter(created_by_id=uid).annotate(
            str_date=Cast('date', TextField())
        ).order_by('date')
        return queryset
        #return Task.objects.filter(created_by_id=uid, date=date, repeated=0) | Task.objects.filter(created_by_id=uid, date=date, repeated=1)

    serializer_class = TaskListSerializer
    permission_classes = [IsOwnerOrReadOnly]


class TaskDetailDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return Task.objects.filter(created_by_id=uid, id=tid).annotate(
            str_date=Cast('date', TextField())
        ).first()
        #return get_object_or_404(Task, created_by_id=uid, id=tid, repeated=0)

    serializer_class = TaskDetailDestroySerializer
    permission_classes = [IsAuthenticated | IsOwnerOrReadOnly]
    http_method_names = ['get', 'delete']


class TaskUpdateView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.request.user.id
        tid = self.kwargs['tid']
        return Task.objects.filter(created_by_id=uid, id=tid).annotate(
            str_date=Cast('date', TextField())
        ).first()

    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']


@api_view(['GET'])
def switch_complete(request, *args, **kwargs):
    uid = request.user.id
    tid = kwargs.get('tid')
    task = get_object_or_404(Task, created_by_id=uid, id=tid)
    task.complete = not task.complete
    task.save()
    # return redirect(f"http://ec2-3-38-100-94.ap-northeast-2.compute.amazonaws.com:8000/task/detail/{tid}") #실제 url
    return redirect(BASE_URL + f"/task/detail/{tid}") #실제 url


@api_view(['GET'])
def switch_tomorrow(request, *args, **kwargs):
    uid = request.user.id
    tid = kwargs.get('tid')
    task = get_object_or_404(Task, created_by_id=uid, id=tid)
    task.date = task.date + datetime.timedelta(days=1)
    task.save()
    # return redirect(f"http://ec2-3-38-100-94.ap-northeast-2.compute.amazonaws.com:8000/task/detail/{tid}") #실제 url
    return redirect(BASE_URL + f"/task/detail/{tid}")  # 실제 url


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


class TaskSearchListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.kwargs['uid']
        if is_following(self.request, uid):
            return Task.objects.filter(created_by_id=uid).annotate(str_date=Cast('date', TextField()))
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
    
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    
class TaskSearchDateListView(generics.ListAPIView):
    def get_queryset(self):
        uid = self.kwargs['uid']
        date = self.kwargs['date']
        if is_following(self.request, uid):
            queryset = Task.objects.filter(created_by_id=uid, date=date).annotate(str_date=Cast('date', TextField()))
            return queryset
        else:
            return ['No permission']
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset == ['No permission']:
            return Response({"detail" : "No permission(folllow)."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # if queryset == ['Empty queryset']:
        #     return Response(data={'detail' : f"No tasks {self.kwargs['date']}"}, status=status.HTTP_200_OK)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class TaskSearchDetailDestroyView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        uid = self.kwargs['uid']
        tid = self.kwargs['tid']
        if is_following(self.request, uid):
            return Task.objects.filter(created_by_id=uid, id=tid).annotate(str_date=Cast('date', TextField())).first()    
        else:
            return "Error"
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == 'Error':
            content = {"detail" : "No permission(folllow)."}
            return HttpResponseBadRequest(json.dumps(content), content_type='application/json')

        if instance == None:
            content = {"detail" : "Invalid task id."}
            return HttpResponseBadRequest(json.dumps(content), content_type='application/json')
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
    serializer_class = TaskDetailDestroySerializer
    permission_classes = [IsAuthenticated | IsOwnerOrReadOnly]
    http_method_names = ['get']       

from django.urls import path

from task.views import TaskListCreateView, TaskListView, TaskDetailDestroyView, TaskUpdateView, \
    switch_complete, switch_tomorrow
    
from task.views import TaskSearchListView, TaskSearchDateListView, TaskSearchDetailDestroyView

urlpatterns = [
    path('list/', TaskListView.as_view()),
    path('list/<date>/', TaskListCreateView.as_view()),
    path('detail/<int:tid>/', TaskDetailDestroyView.as_view()),
    path('detail/<int:tid>/update', TaskUpdateView.as_view()),
    path('detail/<int:tid>/check/', switch_complete),
    path('detail/<int:tid>/delay/', switch_tomorrow),
    
    path('search/<uid>/list/', TaskSearchListView.as_view()),
    path('search/<uid>/list/<date>/', TaskSearchDateListView.as_view()),
    path('search/<uid>/detail/<tid>/', TaskSearchDetailDestroyView.as_view()),
]

    #path('list/repeated', TaskListCreateView.as_view()),
    #path('task/repeated/')
    
    
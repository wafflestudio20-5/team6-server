from django.urls import path

from task.views import TaskListCreateView, TaskListView, TaskDetailDestroyView, TaskUpdateNameView, TaskUpdateDateView, \
    switch_complete, switch_tomorrow

urlpatterns = [
    path('list', TaskListCreateView.as_view()),
    path('list/<date>', TaskListView.as_view()),
    path('<tid>', TaskDetailDestroyView.as_view()),
    path('<tid>/name', TaskUpdateNameView.as_view()),
    path('<tid>/date', TaskUpdateDateView.as_view()),
    path('<tid>/check', switch_complete),
    path('<tid>/delay', switch_tomorrow),

    #path('list/repeated', TaskListCreateView.as_view()),
    #path('task/repeated/')
]
from django.urls import path

from task.views import TaskListCreateView, TaskListView, TaskDetailDestroyView, TaskUpdateNameView, TaskUpdateDateView, \
    switch_complete, switch_tomorrow, TagListCreateView, TagDetailUpdateDestroyView

urlpatterns = [
    path('list', TaskListView.as_view()),
    path('list/<date>', TaskListCreateView.as_view()),
    path('detail/<int:tid>', TaskDetailDestroyView.as_view()),
    path('detail/<int:tid>/name', TaskUpdateNameView.as_view()),
    path('detail/<int:tid>/date', TaskUpdateDateView.as_view()),
    path('detail/<int:tid>/check', switch_complete),
    path('detail/<int:tid>/delay', switch_tomorrow),

    path('tag', TagListCreateView.as_view()),
    path('tag/<int:tid>', TagDetailUpdateDestroyView.as_view())

    #path('list/repeated', TaskListCreateView.as_view()),
    #path('task/repeated/')
]
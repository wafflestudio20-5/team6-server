from django.urls import path

from diary.views import DiaryListView, diary_redirect, DiaryCreateView, DiaryRetrieveUpdateDeleteView

urlpatterns = [
    path('', DiaryListView.as_view()),
    path('<date>', diary_redirect),
    path('<date>/create', DiaryCreateView.as_view()),
    path('<date>/update', DiaryRetrieveUpdateDeleteView.as_view()),
]
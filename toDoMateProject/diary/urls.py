from django.urls import path

from diary.views import DiaryListView, diary_redirect, DiaryListCreateView, DiaryRetrieveUpdateDeleteView, DiaryWatchView, \
    CommentListCreateView, CommentRetrieveUpdateDestroyView ,DiarySearchListView, diary_search_redirect

urlpatterns = [
    path('mydiary/', DiaryListView.as_view()),
    path('mydiary/<date>/', diary_redirect),
    path('mydiary/<date>/create/', DiaryListCreateView.as_view()),
    path('mydiary/<date>/update/', DiaryRetrieveUpdateDeleteView.as_view()),

    path('watch/<did>/', DiaryWatchView.as_view()),
    path('comment/<did>/', CommentListCreateView.as_view()),
    path('comment/detail/<cid>/', CommentRetrieveUpdateDestroyView.as_view()),
    
    path('search/<uid>/', DiarySearchListView.as_view()),
    path('search/<uid>/<date>/', diary_search_redirect),
]
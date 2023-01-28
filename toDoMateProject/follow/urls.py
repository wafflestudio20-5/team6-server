from django.urls import path

from follow.views import FolloweeListView, FollowerListView, follow_user

urlpatterns = [
    path('followee/', FolloweeListView.as_view()),
    path('follower/', FollowerListView.as_view()),
    path('', follow_user)
]

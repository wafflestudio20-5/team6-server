from django.urls import path

from follow.views import (FolloweeListView, FollowerListView, 
                          follow_user, FolloweeDetailView, FollowerDetailView, 
                          block_user, BlockUserListView, BlockDetailView,
                          BlockedUserListView, BlockedDetailView)

urlpatterns = [
    path('follow', follow_user),
    path('followee/list', FolloweeListView.as_view()),
    path('follower/list', FollowerListView.as_view()),
    path('follower/detail/<fid>', FollowerDetailView.as_view()),
    path('followee/detail/<fid>', FolloweeDetailView.as_view()),
    
    path('block', block_user),
    # path('unblock/', unblock_user),
    path('block/list', BlockUserListView.as_view()),
    path('block/detail/<fid>', BlockDetailView.as_view()), 
    path('blocked/list', BlockedUserListView.as_view()),
    path('blocked/detail/<fid>', BlockedDetailView.as_view())    
]

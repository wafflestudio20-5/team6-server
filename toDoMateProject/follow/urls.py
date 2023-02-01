from django.urls import path

from follow.views import FolloweeListView, FollowerListView, follow_user, unfollow_user, FolloweeDetailView, FollowerDetailView, block_user, unblock_user, BlockUserListView, IsBlockingNowDetailView

urlpatterns = [
    path('followee/', FolloweeListView.as_view()),
    path('follower/', FollowerListView.as_view()),
    path('', follow_user),
    path('follower/<fid>/', FollowerDetailView.as_view()),
    path('followee/<fid>/', FolloweeDetailView.as_view()),
    path('unfollow/', unfollow_user),
    
    path('block/', block_user),
    path('unblock/', unblock_user),
    path('block/list/', BlockUserListView.as_view()),
    path('block/detail/<fid>/', IsBlockingNowDetailView.as_view())    
]

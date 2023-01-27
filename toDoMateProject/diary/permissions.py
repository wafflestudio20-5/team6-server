from rest_framework import permissions
from follow.models import Follow

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            uid = request.user.id
            # 팔로우 하고 있는 사람의 diary는 볼 수 있음.
            followers = [obj.to_user.id for obj in Follow.objects.filter(from_user=uid)]            
            if obj.created_by_id in followers:
                return True
            else:
                return False

        return False
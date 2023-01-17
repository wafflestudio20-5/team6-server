from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
            #팔로우 시 True로 수정

        return False
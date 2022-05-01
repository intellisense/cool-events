from rest_framework import permissions


class CanManageEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class CanManageEventParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = obj.event.owner == request.user
        is_participant = obj.user == request.user

        if is_owner and is_participant:
            return False

        return is_owner or is_participant

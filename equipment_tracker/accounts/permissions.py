from rest_framework.permissions import BasePermission


class IsTechnician(BasePermission):
    message = "You must be a technician to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_technician

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_technician

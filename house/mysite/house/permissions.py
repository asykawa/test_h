from rest_framework import permissions

class CreateReview(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role in ['buyer', 'admin']:
            return True
        return False
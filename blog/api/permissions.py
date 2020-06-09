from rest_framework import permissions


class AuthorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                return True

        case_1 = obj.author == request.user
        case_2 = request.user.is_superuser
        case_3 = request.user.is_staff
        if case_1 or case_2 or case_3:
            return True


class UserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                return True

        case_1 = obj.user == request.user
        case_2 = request.user.is_superuser
        case_3 = request.user.is_staff
        if case_1 or case_2 or case_3:
            return True

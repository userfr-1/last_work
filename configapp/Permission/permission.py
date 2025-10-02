from django.core.cache import cache
from rest_framework.permissions import BasePermission
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
        )

class IsEmailVerified(BasePermission):
    message = "Avval emailingizni verify qiling!"

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated and (user.is_superuser or user.is_staff):
            return True
        email = request.data.get("email") or request.query_params.get("email")
        if not email and "user" in request.data:
            email = request.data["user"].get("email")
        if not email and user and user.is_authenticated:
            email = user.email

        if not email:
            return False

        return cache.get(f"{email}_verified", False)


class IsLoggedInUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
class IsStudentPermission(BasePermission):
    message = "Siz student emassiz"  # default xabar

    def has_permission(self, request, view):
        if getattr(request.user, "is_student", False):
            if request.user.is_active:
                return True
            else:
                self.message = "Avval passwordni o'zgartiring!"
                return False
        return False
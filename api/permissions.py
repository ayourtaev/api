from rest_framework.permissions import BasePermission
from api.models import AuthToken


class AuthTokenKeeper(BasePermission):
    message = "Wrong auth token"

    def has_permission(self, request, view):
        # Authorization
        auth = request.META.get('HTTP_AUTHORIZATION')
        if AuthToken.objects.filter(token=auth).first():
            return True


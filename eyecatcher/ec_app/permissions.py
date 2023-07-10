from rest_framework import permissions

from .models import System, Report


class OwnSystemOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the system, but anyone can register a new system
        if isinstance(obj, Report):
            return obj.system.verify_auth_code(request.data.get('auth_code'), request.data.get('system'))
        if view.action == 'create':
            return True
        if isinstance(obj, System):
            return obj.verify_auth_code(request.data.get('auth_code'), request.data.get('system'))
        return False

from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite acceso si el usuario es admin o es dueño del objeto.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        # Si el objeto tiene campo created_by
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        # Si el objeto tiene responsable
        if hasattr(obj, 'responsible'):
            return obj.responsible == request.user
        return False

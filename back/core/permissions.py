from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrCustomerReadOnly(BasePermission):
    """Allow full access to admin users.

    Allow GET (safe) methods to authenticated users that have a related
    `customer` object (see `core.models.Customer`). Deny otherwise.
    """

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False

        # Admins (staff / superuser) get full access
        if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
            return True

        # Customers may only use safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS and hasattr(user, 'customer'):
            return True

        return False

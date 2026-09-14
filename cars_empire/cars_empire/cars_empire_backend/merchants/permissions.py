from rest_framework import permissions

class IsMerchantOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a merchant to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the merchant
        # Check if the user is a merchant user with admin role
        return obj.users.filter(
            user=request.user,
            role='admin',
            is_active=True
        ).exists() 
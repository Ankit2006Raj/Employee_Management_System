from rest_framework import permissions


class IsHROrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow HR staff to edit objects.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions are only allowed to HR staff
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.groups.filter(name='HR').exists()
        )


class IsManagerOrHR(permissions.BasePermission):
    """
    Custom permission to allow managers and HR to access certain resources.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # HR and staff have full access
        if request.user.is_staff or request.user.groups.filter(name='HR').exists():
            return True
        
        # Managers can access their subordinates
        if hasattr(request.user, 'employee_profile'):
            employee = request.user.employee_profile
            if hasattr(obj, 'manager') and obj.manager == employee:
                return True
            if hasattr(obj, 'employee') and obj.employee.manager == employee:
                return True
        
        # Users can access their own data
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if hasattr(obj, 'employee') and hasattr(obj.employee, 'user') and obj.employee.user == request.user:
            return True
        
        return False


class IsOwnerOrHR(permissions.BasePermission):
    """
    Custom permission to allow users to edit their own profile or HR to edit any profile.
    """
    
    def has_object_permission(self, request, view, obj):
        # HR and staff have full access
        if request.user.is_staff or request.user.groups.filter(name='HR').exists():
            return True
        
        # Users can only edit their own profile
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False

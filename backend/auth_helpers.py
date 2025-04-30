from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(roles):
    """
    A decorator to check if the current user has the required role(s)
    
    Args:
        roles (str or list): A single role or list of roles that are allowed to access the route
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT is present and valid
            verify_jwt_in_request()
            
            # Get claims from JWT
            claims = get_jwt()
            
            # Check if user role is in the required roles
            if isinstance(roles, str):
                required_roles = [roles]
            else:
                required_roles = roles
                
            if claims.get('role') not in required_roles:
                return jsonify({"msg": "Access denied: insufficient permissions"}), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Predefined role decorators for common use cases
def admin_required(fn):
    """Decorator to require admin role"""
    return role_required('admin')(fn)

def manager_required(fn):
    """Decorator to require manager role or higher"""
    return role_required(['admin', 'manager'])(fn)

def user_required(fn):
    """Decorator to require user role or higher"""
    return role_required(['admin', 'manager', 'user'])(fn)

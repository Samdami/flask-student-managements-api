from ..models.users import User
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from http import HTTPStatus

# Get the user type for use in the @admin() decorator
def get_user_type(id:int):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.user_type
    else:
        return None

# Custom decorator to verify admin access
def admin():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            else:
                return {"message": "Administrator access required"}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper
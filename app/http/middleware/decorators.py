from functools import wraps
from flask import request, url_for, jsonify
from flask_login import login_required, current_user
from cerberus import Validator


def validate_access(level=0):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.access_level >= level:
                return f(*args, **kwargs)
            return url_for('home.login', next=request.url)
        return decorated_function
    return decorator



def validate_request(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            validator = Validator(schema)
            try:
                data = request.get_json(force=True)
            except:
                data = dict()
            data = data if data else dict(request.args)
            if validator.validate(data):
                return f(data=data, *args, **kwargs)
            return jsonify(validator.errors), 400
        return wrapper
    return decorator

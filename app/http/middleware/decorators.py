from functools import wraps, update_wrapper
from flask import request, url_for, jsonify, redirect
from flask_login import login_required, current_user
from cerberus import Validator


def validate_access(level=1):
    def decorator(f):
        @wraps(f)
        @login_required
        def authorize(*args, **kwargs):
            if current_user.access_level >= level:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('login.login'))
        return authorize
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
            # if the request is empty check the url
            if (not data):
                data = dict(request.args)
            if validator.validate(data):
                return f(data=data, *args, **kwargs)
            # else there was an error
            else:
                return jsonify(validator.errors), 400
        return wrapper
    return decorator

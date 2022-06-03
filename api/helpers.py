from functools import wraps

import jwt as jwt
from flask import request, abort


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        return f("test", *args, **kwargs)
        if 'Authorization' not in request.headers:
            abort(401)

        user = None
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        try:
            pass
            # Authentication logic
            # user = jwt.decode(token, config.main.SECRET, algorithms=['HS256'])['sub']
        except Exception as e:
            print(e)
            abort(401)

        self, *rest = args
        return f(self, user, *rest, **kwargs)

    return decorator


def expect(fields: set):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return {
                           'error': 'accepts only application/json requests.'
                       }, 400

            if not fields.issubset(request.json):
                difference = fields.difference(request.json)
                return {
                           'error': f'{", ".join(difference)}'
                                    f'{" is" if len(difference) == 1 else " are"} missing from request body'
                       }, 400

            return f(*args, **request.json, **kwargs)

        return decorated_function

    return decorator

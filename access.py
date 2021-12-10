from functools import wraps
from flask import session, current_app, request, render_template


def is_group_permission_valid():
    config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('group_name', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[-1]
    if group_name in config and target_app in config[group_name]:
        return True
    return False


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_group_permission_valid():
            return f(*args, **kwargs)
        message = {'message': 'Permission denied'}
        return render_template('notification.html', message=message)
    return wrapper


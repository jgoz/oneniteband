from cryptacular.bcrypt import BCRYPTPasswordManager
from flask import Flask, g, redirect, render_template, request, session, url_for
from functools import wraps

class RestFlask(Flask):
    def get(self, rule, **options):
        return self._rest_route(rule, 'GET', **options)

    def post(self, rule, **options):
        return self._rest_route(rule, 'POST', **options)

    def put(self, rule, **options):
        return self._rest_route(rule, 'PUT', **options)

    def delete(self, rule, **options):
        return self._rest_route(rule, 'DELETE', **options)

    def _rest_route(self, rule, method, **options):
        options.update(methods=[method])
        return self.route(rule, **options)

def templated(template=None):
    """Specifies template to use so that locals dictionary can be returned."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint.replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

def login_required(f):
    """Indicates user must be logged in to access view."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user'] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_password(user, password):
    if not user:
        raise 'User `' + username + '` not found.'
    bcrypt = BCRYPTPasswordManager()
    if not bcrypt.check(user.hash, password):
        raise 'Password given for `' + username + '` does not match.'
    return True

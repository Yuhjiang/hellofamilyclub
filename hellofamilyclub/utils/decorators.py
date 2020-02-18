from functools import wraps

from django.shortcuts import redirect


def admin_required(function, redirect_url='/'):
    @wraps(function)
    def wrapped_function(request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect(redirect_url)
    return wrapped_function

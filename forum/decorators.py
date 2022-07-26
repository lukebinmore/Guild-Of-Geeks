from . import functions as f
from functools import wraps
from django.contrib import messages

def login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You must be logged into view this page!')
            return f.redirect_page(request, 'index')
    return wrap
from . import functions as f
from functools import wraps
from django.contrib import messages
from . import models

def login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You must be logged into view this page!')
            return f.redirect_page(request, 'index')
    return wrap

def check_post_author(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        slug = kwargs['slug']
        post = f.get_object(models.Post, slug=slug)

        if post.author == request.user or request.user.is_staff:
            return function(request, *args, **kwargs)
        
        messages.error(request, 'This item does not belong to you!')
        return f.redirect_page(request, 'index')
    return wrap

def check_comment_author(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        id = kwargs['id']
        comment = f.get_object(models.Comment, id=id)
        if comment.author == request.user or request.user.is_staff:
            return function(request, *args, **kwargs)
        
        messages.error(request, 'This item does not belong to you!')
        return f.redirect_page(request, 'index')
    return wrap

def check_ajax(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if f.check_if_ajax_request(request):
            return function(request, *args, **kwargs)
        messages.error(request, 'This action is not allowed in this way!')
        return f.redirect_page(request, 'index')
    return wrap

from . import functions as f
from functools import wraps
from django.contrib import messages
from . import models


def login_required(function):
    """
    If the user is logged in, return the function, otherwise redirect to the
    index page

    :param function: The function that is being decorated
    :return: A function that wraps the function passed in as an argument.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, "You must be logged into view this page!")
            return f.redirect_page(request, "index")

    return wrap


def check_post_author(function):
    """
    If the user is not the author of the post, or if the user is not a staff
    member, then redirect the
    user to the index page

    :param function: The function that is being decorated
    :return: The function is being returned.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        slug = kwargs["slug"]
        if slug == "new-post":
            return function(request, *args, **kwargs)

        post = f.get_object(models.Post, slug=slug)

        if post.author == request.user or request.user.is_staff:
            return function(request, *args, **kwargs)

        messages.error(request, "This item does not belong to you!")
        return f.redirect_page(request, "index")

    return wrap


def check_comment_author(function):
    """
    If the comment's author is the same as the user who is logged in, or if
    the user is a staff member,
    then the function will be executed. Otherwise, an error message will be
    displayed and the user will
    be redirected to the index page

    :param function: The function that is being decorated
    :return: The function is being returned.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        id = kwargs["id"]
        comment = f.get_object(models.Comment, id=id)
        if comment.author == request.user or request.user.is_staff:
            return function(request, *args, **kwargs)

        messages.error(request, "This item does not belong to you!")
        return f.redirect_page(request, "index")

    return wrap


def check_ajax(function):
    """
    If the request is an ajax request, then return the function, otherwise
    return an error message and
    redirect to the index page

    :param function: The function that is being decorated
    :return: A function that wraps the function passed in as an argument.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if f.check_if_ajax_request(request):
            return function(request, *args, **kwargs)
        messages.error(request, "This action is not allowed in this way!")
        return f.redirect_page(request, "index")

    return wrap

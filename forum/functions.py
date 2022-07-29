from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from . import models


def previous_page(request):
    """
    It renders a template that redirects to the URL that was requested

    :param request: The request object
    :return: The previous page.
    """
    return render(
        request,
        "redirect.html",
        {"redirect_url": request.META["HTTP_HX_CURRENT_URL"]},
    )


def redirect_page(request, page, **kwargs):
    """
    It renders a template that contains a meta refresh tag that redirects to
    the page specified by the page parameter.

    :param request: The request object
    :param page: The name of the page you want to redirect to
    :return: A function that takes a request and a page and
    returns a render function.
    """
    return render(
        request,
        "redirect.html",
        {"redirect_url": reverse(page, kwargs=kwargs)},
    )


def check_if_ajax_request(request):
    """
    It checks if the request is an AJAX request.

    :param request: The request object
    """
    if request.META["HTTP_ACCEPT"] == "*/*":
        return True
    return False


def form_field_errors(*args):
    """
    A decorator function.
    """
    for form in args:
        for field in form:
            if field.errors:
                return f"{field.name.title()} : {field.errors[0]}"


def get_object(model, **kwargs):
    """
    It returns an object from the database.

    :param model: The model class
    """
    queryset = model.objects.all()
    return get_object_or_404(queryset, **kwargs)


def validate_category(form, title):
    """
    It validates the category.

    :param form: The form that is being validated
    :param title: The title of the category
    """
    if not title.isdigit():
        if not models.Category.objects.filter(title=title).exists():
            category = models.Category.objects.create(title=title)
            form.set_category(category)
    else:
        if not models.Category.objects.filter(id=title).exists():
            del form.errors["category"][0]
            form.add_error("category", "Category can not be numbers only!")
    return form


def validate_tags(form, tags):
    """
    It validates the tags.

    :param form: The form object
    :param tags: a list of strings
    """
    new_tags = []
    for tag in tags:
        if not tag.isdigit():
            if not models.Tag.objects.filter(title=tag).exists():
                new_tags.append(models.Tag.objects.create(title=tag))
        else:
            if not models.Tag.objects.filter(id=tag).exists():
                del form.errors["tags"][0]
                form.add_error("tags", "Tags may not be just numbers!")
            else:
                new_tags.append(tag)
    form.set_tags(new_tags)
    return form


def validate_username(form):
    """
    It validates the username.

    :param form: The form object that is being validated
    """
    username = form.data["username"]

    if " " in username:
        form.add_error("username", "Username cannot contain spaces.")
    if len(username) < 6:
        form.add_error(
            "username", "Username must be a minimum of 6 characters."
        )
    if len(username) > 14:
        form.add_error(
            "username", "Username must be a maximum of 14 characters."
        )
    if any(not c.isalnum() for c in username):
        form.add_error(
            "username", "Username must not contain special characters."
        )
    return form


def validate_password(form, form_field):
    """
    It validates the password.

    :param form: The form object
    :param form_field: The field that is being validated
    """
    password = form.data[form_field]

    if " " in password:
        form.add_error(form_field, "Password cannot contain spaces.")
    if len(password) < 8:
        form.add_error(
            form_field, "Password must be a minimum of 8 characters."
        )
    if len(password) > 25:
        form.add_error(
            form_field, "Password must be a maximum of 25 characters."
        )
    if not any(not c.isalnum() for c in password):
        form.add_error(
            form_field,
            "Password must contain at least one special character. (E.G. @)",
        )
    return form

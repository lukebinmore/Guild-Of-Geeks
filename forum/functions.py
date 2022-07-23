from django.shortcuts import render
from django.urls import reverse

def previous_page(request):
    return render(
        request,
        'redirect.html',
        {
            'redirect_url': request.META['HTTP_HX_CURRENT_URL']
        }
    )

def form_field_errors(form):
    for field in form:
        if field.errors:
            return f'{field.name.title()} : {field.errors[0]}'    return render(
        request,
        'redirect.html',
        {
            'redirect_url': reverse(page, kwargs=kwargs)
        }
    )

def form_field_errors(*args):
